import shutil
import os

class Path:

    @staticmethod
    def copy_from_to(from_path: str, to_path: str) -> None:

        """
        :param from_path: file that should be copied
        :param to_path: destination path
        """

        shutil.copy(from_path, to_path) #! copy file from - to

    @staticmethod
    def get_all_folder_names(path: str) -> list:

        """
        :param path: a path to list all items in it
        :return: names of all folders in a certain path
        """

        names = [] #! list for all names

        for item in os.listdir(path): #! for every item in a certain path

            full_path = os.path.join(path, item) #! create full path

            if os.path.isdir(full_path): #! check if its a folder and not a file

                names.append(item) #! add to list

        return names
    
    @staticmethod
    def slice_path(input_path: str) -> list:

        """
        :param input path: path that should be sliced
        :return: parts of a path
        """

        path = Path(input_path) #! class from pathlib to get all parts from a path in a list
        parts = path.parts  #! get only parts from object

        return parts
    
class File:

    class txt:

        pass

    class json:

        pass

    class toml:

        pass

    class yaml:

        pass
    