import logging
import re
import warnings
from pathlib import Path
from typing import Callable, Literal, Union

import h5py
import numpy as np
import pandas as pd
import scipy.constants as cn
from tqdm import tqdm
from tqdm.notebook import tqdm as notebook_tqdm

from emout.utils import InpFile, RegexDict, UnitConversionKey, Units, UnitTranslator

from .griddata_series import GridDataSeries
from .vector_data import VectorData2d

logger = logging.getLogger(__name__)


def get_tqdm():
    """Function to determine the appropriate tqdm version."""
    try:
        # Check if the environment is Jupyter Notebook
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == "ZMQInteractiveShell":  # Jupyter Notebook environment
            logger.debug("Jupyter Notebook environment detected.")
            return notebook_tqdm
        else:  # IPython environment, but not Jupyter Notebook
            logger.debug("IPython environment detected (not Jupyter).")
            return tqdm
    except NameError:  # IPython is not available = standard Python environment
        logger.debug("Standard Python environment detected.")
        return tqdm


# Get the appropriate tqdm
tqdm = get_tqdm()


def t_unit(out: "Emout") -> UnitTranslator:
    """tの単位変換器を生成する.

    Parameters
    ----------
    out : Emout
        Emoutオブジェクト

    Returns
    -------
    UnitTranslator
        tの単位変換器
    """
    return (out.unit.t * UnitTranslator(out.inp.ifdiag * out.inp.dt, 1)).set_name(
        "t", unit="s"
    )


def wpet_unit(out: "Emout") -> UnitTranslator:
    """wpe * tの単位変換器を生成する.

    以下のコードを実行することで、データのt軸をwpe*tで規格化できる.

    >>> Emout.name2unit['t'] = wpet_unit

    Parameters
    ----------
    out : Emout
        Emoutオブジェクト

    Returns
    -------
    UnitTranslator
        wpe * tの単位変換器
    """
    return UnitTranslator(
        out.inp.wp[0] * out.inp.ifdiag * out.inp.dt, 1, name="wpe * t", unit=""
    )


def wpit_unit(out: "Emout") -> UnitTranslator:
    """wpi * tの単位変換器を生成する.

    以下のコードを実行することで、データのt軸をwpe*tで規格化できる.

    >>> Emout.name2unit['t'] = wpit_unit

    Parameters
    ----------
    out : Emout
        Emoutオブジェクト

    Returns
    -------
    UnitTranslator
        wpi * tの単位変換器
    """
    return UnitTranslator(
        out.inp.wp[1] * out.inp.ifdiag * out.inp.dt, 1, name="wpi * t", unit=""
    )


def none_unit(out: "Emout") -> UnitTranslator:
    return UnitTranslator(1, 1, name="", unit="")


def ndp_unit(ispec: int) -> Callable[["Emout"], UnitTranslator]:
    def ndp_unit(out: "Emout") -> UnitTranslator:
        wp = out.unit.f.reverse(out.inp.wp[ispec])
        mp = abs(cn.m_e / out.inp.qm[ispec])
        np = wp**2 * mp * cn.epsilon_0 / cn.e**2
        return UnitTranslator(np * 1e-6, 1.0, name="number density", unit="/cc")

    return ndp_unit


def nd3p_unit(out: "Emout") -> UnitTranslator:
    wpp = out.unit.f.reverse(out.inp.wp[2])
    np = wpp**2 * cn.m_e * cn.epsilon_0 / cn.e**2
    return UnitTranslator(np * 1e-6, 1.0, name="number density", unit="/cc")


class Emout:
    """EMSES出力・inpファイルを管理する.

    Attributes
    ----------
    directory : Path
        管理するディレクトリ
    dataname : GridData
        3次元データ(datanameは"phisp"などのhdf5ファイルの先頭の名前)
    """

    name2unit = RegexDict(
        {
            r"phisp": lambda self: self.unit.phi,
            # r'nd[12]p': ndp_unit,
            r"nd1p": ndp_unit(0),
            r"nd2p": ndp_unit(1),
            r"nd3p": ndp_unit(2),
            r"nd4p": ndp_unit(3),
            r"nd5p": ndp_unit(4),
            r"nd6p": ndp_unit(5),
            r"nd7p": ndp_unit(6),
            r"nd8p": ndp_unit(7),
            r"nd9p": ndp_unit(8),
            r"rho": lambda self: self.unit.rho,
            r"rhobk": lambda self: self.unit.rho,
            r"j.*": lambda self: self.unit.J,
            r"b[xyz]": lambda self: self.unit.H,
            r"rb[xyz]": lambda self: self.unit.H,
            r"e[xyz]": lambda self: self.unit.E,
            r"re[xyz]": lambda self: self.unit.E,
            r"t": t_unit,
            r"axis": lambda self: self.unit.length,
            r"rhobksp[1-9]": lambda self: self.unit.rho,
        }
    )

    def __init__(
        self, directory="./", append_directories=None, ad=None, inpfilename="plasma.inp"
    ):
        """EMSES出力・inpファイルを管理するオブジェクトを生成する.

        Parameters
        ----------
        directory : str or Path
            管理するディレクトリ, by default './'
        append_directories : list(str) or list(Path) or "auto"
            管理する継続ディレクトリのリスト, by default []
        ad : list(str) or list(Path) or "auto"
            管理する継続ディレクトリのリスト, by default []
        inpfilename : str, optional
            パラメータファイルの名前, by default 'plasma.inp'
        """
        if not isinstance(directory, Path):
            directory = Path(directory)
        self.directory = directory
        logger.info(
            f"Initializing Emout object for directory: {self.directory.resolve()}"
        )

        append_directories = append_directories or ad

        if append_directories == "auto":
            append_directories = self.__fetch_append_directories(directory)

        if append_directories is None:
            append_directories = []

        self.append_directories = []

        for append_directory in append_directories:
            if not isinstance(append_directory, Path):
                append_directory = Path(append_directory)
            self.append_directories.append(append_directory)

        # パラメータファイルの読み取りと単位変換器の初期化
        self.__load_inpfile(inpfilename)

    def __fetch_append_directories(self, directory: Path):
        logger.info(f"Fetching append directories for: {directory}")
        append_directories = []

        i = 2
        while True:
            path_next = f"{str(directory.resolve())}_{i}"
            directory_next = Path(path_next)

            if not directory_next.exists():
                logger.debug(f"Append directory does not exist: {directory_next}")
                break

            next_data = Emout(directory_next)
            if not next_data.is_valid():
                logger.warning(
                    f"{directory_next.resolve()} exists, but it is not valid directory."
                )
                break

            append_directories.append(directory_next)

            i += 1

        return append_directories

    def __load_inpfile(self, inpfilename: str):
        self._inp: Union[InpFile, None] = None
        self._unit: Union[Units, None] = None

        if inpfilename is None:
            return

        inpfilepath = self.directory / inpfilename

        if not inpfilepath.exists():
            return

        logger.info(f"Loading parameter file: {inpfilepath.resolve()}")
        self._inp = InpFile(inpfilepath)

        convkey = UnitConversionKey.load(inpfilepath)
        if convkey is not None:
            self._unit = Units(dx=convkey.dx, to_c=convkey.to_c)

    def __getattr__(self, __name: str) -> "GridDataSeries":
        logger.debug(f"Accessing attribute: {__name}")

        m = re.match(r"^r([eb][xyz])$", __name)
        if m:
            logger.debug(f"Relocated field requested: {m.group(1)}")
            self.__create_relocated_field_hdf5(m.group(1))

        m = re.match(r"(.+)([xyz])([xyz])$", __name)
        if m:
            logger.debug(f"Creating VectorData2d for: {__name}")
            dname = m.group(1)
            axis1 = m.group(2)
            axis2 = m.group(3)
            vector_data = VectorData2d(
                [getattr(self, f"{dname}{axis1}"), getattr(self, f"{dname}{axis2}")],
                name=__name,
            )

            setattr(self, f"_{__name}", vector_data)

            return vector_data

        filepath = self.__fetch_filepath(self.directory, f"{__name}00_0000.h5")
        logger.info(f"Loading grid data from file: {filepath.resolve()}")
        griddata = self.__load_griddata(filepath)

        for append_directory in self.append_directories:
            filepath = self.__fetch_filepath(append_directory, f"{__name}00_0000.h5")
            griddata_append = self.__load_griddata(filepath)

            griddata = griddata.chain(griddata_append)

        setattr(self, f"_{__name}", griddata)

        return griddata

    def __create_relocated_field_hdf5(self, name: str) -> None:
        axis = "zyx".index(name[-1])

        btype = ["periodic", "dirichlet", "neumann"][self.inp.mtd_vbnd[2 - axis]]

        filepath = self.__fetch_filepath(self.directory, f"{name}00_0000.h5")
        _create_relocated_field_hdf5(filepath.parent, name=name, axis=axis, btype=btype)

        for append_directory in self.append_directories:
            filepath = self.__fetch_filepath(append_directory, f"{name}00_0000.h5")
            _create_relocated_field_hdf5(
                filepath.parent, name=name, axis=axis, btype=btype
            )

    def __fetch_filepath(self, directory: Path, pattern: str) -> Path:
        filepathes = list(directory.glob(pattern))
        if len(filepathes) == 0:
            raise Exception(f"{pattern} is not found.")
        if len(filepathes) >= 2:
            raise Exception(
                f"There are multiple files that satisfy {pattern}.  Please specify so that just one is specified."
            )

        filepath = filepathes[0]

        return filepath

    def __load_griddata(self, h5file_path: Path) -> "GridDataSeries":
        if self.unit is None:
            tunit = None
            axisunit = None
        else:
            tunit = Emout.name2unit.get("t", lambda self: None)(self)
            axisunit = Emout.name2unit.get("axis", lambda self: None)(self)

        name = str(h5file_path.name).replace("00_0000.h5", "")

        if self.unit is None:
            valunit = None
        else:
            valunit = Emout.name2unit.get(name, lambda self: None)(self)

        data = GridDataSeries(
            h5file_path, name, tunit=tunit, axisunit=axisunit, valunit=valunit
        )

        return data

    @property
    def inp(self) -> Union[InpFile, None]:
        """パラメータの辞書(Namelist)を返す.

        Returns
        -------
        InpFile or None
            パラメータの辞書(Namelist)
        """
        return self._inp

    def is_valid(self) -> bool:
        """シミュレーションが正常に終了しているか判定する.

        Note:
            icurが最終ステップまで出力されているかで判定しており、hdf5ファイルだけが壊れている場合など判定が間違う場合がある。

        Returns
        -------
        bool
            シミュレーションが正常に終了している場合True
        """

        def read_last_line(file_name):
            with open(file_name, "rb") as f:
                f.seek(-2, 2)
                while f.read(1) != b"\n":
                    f.seek(-2, 1)
                return f.readline().decode("utf-8")

        if len(self.append_directories) > 0:
            dirpath = self.append_directories[-1]
        else:
            dirpath = self.directory

        if not (dirpath / "icur").exists():
            return False

        try:
            last_line = read_last_line(dirpath / "icur")
        except OSError:
            return False

        inp = InpFile(dirpath / "plasma.inp")

        return int(last_line.split()[0]) == int(inp.nstep)

    @property
    def unit(self) -> Union[Units, None]:
        """単位変換オブジェクトを返す.

        Returns
        -------
        Units or None
            単位変換オブジェクト
        """
        return self._unit

    @property
    def icur(self) -> pd.DataFrame:

        names = []
        for ispec in range(self.inp.nspec):
            names.append(f"{ispec+1}_step")
            for ipc in range(self.inp.npc):
                names.append(f"{ispec+1}_body{ipc+1}")
                names.append(f"{ispec+1}_body{ipc+1}_ema")

        df = pd.read_csv(self.directory / "icur", sep="\s+", header=None, names=names)

        return df

    @property
    def pbody(self) -> pd.DataFrame:
        names = ["step"] + [f"body{i+1}" for i in range(self.inp.npc + 1)]

        df = pd.read_csv(self.directory / "pbody", sep="\s+", names=names)

        return df


def _create_relocated_field_hdf5(
    directory: Path,
    name: str,
    axis: int,
    btype: Literal["periodic", "dirichlet", "neumann"],
):
    if name.startswith("b"):
        relocated = relocated_magnetic_field
    elif name.startswith("e"):
        relocated = relocated_electric_field

    input_filepath = directory / f"{name}00_0000.h5"
    output_filepath = directory / f"r{name}00_0000.h5"

    if output_filepath.exists():
        logger.info(f"File already exists: {output_filepath.resolve()}")
        return

    logger.info(
        f"Relocated field file not found. Creating a new file.: {output_filepath.resolve()}"
    )

    with h5py.File(input_filepath, "r") as h5_field:
        field = h5_field[name]

        with h5py.File(output_filepath, "w") as h5_relocated:
            rfield = h5_relocated.create_group(f"r{name}")

            for key in tqdm(field.keys(), desc=f"Relocating {name}"):
                rfield[key] = relocated(
                    np.array(field[key]),
                    axis=axis,
                    btype=btype,
                )

    logger.info(f"File creation completed: {output_filepath.resolve()}")


def relocated_electric_field(
    ef: np.ndarray, axis: int, btype: Literal["periodic", "dirichlet", "neumann"]
):
    def slc(a, b=None):
        s = slice(a, b) if b else a
        slices = tuple(s if i == axis else slice(None, None) for i in range(3))

        return slices

    # Relocated electric field buffer
    ref = np.zeros_like(ef)

    ref[slc(1, -1)] = 0.5 * (ef[slc(None, -2)] + ef[slc(1, -1)])

    if btype in "periodic":
        ref[slc(0)] = 0.5 * (ef[slc(-2)] + ef[slc(1)])
        ref[slc(-1)] = 0.5 * (ef[slc(-2)] + ef[slc(1)])
    elif btype in "neumann":
        ref[slc(0)] = 0
        ref[slc(-1)] = 0
    else:
        ref[slc(0)] = ef[slc(1)]
        ref[slc(-1)] = ef[slc(-2)]

    return ref


def relocated_magnetic_field(
    bf: np.array, axis: int, btype: Literal["periodic", "dirichlet", "neumann"]
):
    def slc(s1, s2=slice(None, None)):
        axis1 = (axis + 1) % 3
        axis2 = (axis + 2) % 3

        slices = [None, None, None]

        slices[axis] = slice(None, None)
        slices[axis1] = s1
        slices[axis2] = s2
        slices = tuple(slices)

        return slices

    # Relocated electric field buffer
    rbf = np.zeros_like(bf)

    # xy平面に1グリッド覆うように拡張する
    bfe = np.empty(
        np.array(bf.shape) + np.array([0 if i == axis else 1 for i in range(3)])
    )
    bfe[slc(slice(1, -1), slice(1, -1))] = bf[slc(slice(None, -1), slice(None, -1))]
    if btype in "periodic":
        bfe[slc(slice(1, -1), 0)] = bfe[slc(slice(1, -1), -2)]
        bfe[slc(slice(1, -1), -1)] = bfe[slc(slice(1, -1), 1)]
    elif btype in "dirichlet":
        bfe[slc(slice(1, -1), 0)] = -bfe[slc(slice(1, -1), 1)]
        bfe[slc(slice(1, -1), -1)] = -bfe[slc(slice(1, -1), -2)]
    else:  # if btype in "neumann":
        bfe[slc(slice(1, -1), 0)] = bfe[slc(slice(1, -1), 1)]
        bfe[slc(slice(1, -1), -1)] = bfe[slc(slice(1, -1), -2)]

    if btype in "periodic":
        bfe[slc(0)] = bfe[slc(-2)]
        bfe[slc(-1)] = bfe[slc(1)]
    elif btype in "dirichlet":
        bfe[slc(0)] = -bfe[slc(1)]
        bfe[slc(-1)] = -bfe[slc(-2)]
    else:  # if btype in "neumann":
        bfe[slc(0)] = bfe[slc(1)]
        bfe[slc(-1)] = bfe[slc(-2)]

    rbf[:, :, :] = 0.25 * (
        bfe[slc(slice(None, -1), slice(None, -1))]
        + bfe[slc(slice(1, None), slice(None, -1))]
        + bfe[slc(slice(None, -1), slice(1, None))]
        + bfe[slc(slice(1, None), slice(1, None))]
    )

    return rbf
