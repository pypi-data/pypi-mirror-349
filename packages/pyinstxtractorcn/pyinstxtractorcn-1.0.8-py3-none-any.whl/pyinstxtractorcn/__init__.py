from .cli import (
    PyInstExtractorError,
    InvalidFileError,
    ExtractionError,
    dcp as _dcp
)

__version__ = "1.0.7"
__all__ = ["dcp", "PyInstExtractorError", "InvalidFileError", "ExtractionError"]

def dcp(file_path: str, output_dir: str = None) -> str:
    """
    解包PyInstaller生成的可执行文件
    
    :param file_path: 目标文件路径
    :param output_dir: 自定义输出目录
    :return: 解包目录绝对路径
    """
    try:
        return _dcp(file_path, output_dir)
    except PyInstExtractorError:
        raise
    except Exception as e:
        raise PyInstExtractorError(str(e)) from e

if __name__ == "__main__":
    from .cli import main
    main()