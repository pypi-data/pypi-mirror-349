"""
===============================================================================
InputModifier Class

Authors: Lloyd Fletcher, Rory Spencer
===============================================================================
"""
from pathlib import Path


class InputModifier:
    """
    Class to modify variables in generic text-based input files.

    Once variables have been modified by the user by passing in a dictionary of
    new variables the input can be written to file.

    Variable definition blocks should begin #comment character#* and end
    #comment character#**, e.g. //_* and //** for gmsh or #_* and #** for
    moose.
    """

    def __init__(
        self,
        input_file: Path,
        comment_char="#",
        end_char="",
        var_start="_*",
        var_end="**",
    ) -> None:
        """Initialise the class by reading in the input file. Find and read
        any variables that are at the top of the file. Default comment_char
        and end_char are set based on reading MOOSE *.i files.

        Args:
            input_file (str): Path to the input text file.
            comment_char (str): character(s) describing what a comment look
                like in the file.
            end_char (str): character (if any) that ends a line, i.e. ; for gmsh
            var_start (str): character sequence used to specify the start of
                the variable block to edit.
            var_end (str): character sequence used to specify the end of the
                variabled block to edit.
        """
        self._vars = dict({})
        self._input_file = input_file

        with open(self._input_file, "r", encoding="utf-8") as in_file:
            self._input_lines = in_file.readlines()

        self._comment_char = comment_char
        self._end_char = end_char

        self._var_start_str = var_start
        self._var_end_str = var_end

        self._var_start_ind = 0
        self._var_end_ind = -1

        self.find_vars()
        self.read_vars()

    def _extract_var_str(self, var_line: str) -> tuple[str, str | float | int, str]:
        """Helper function to split a string from the input file variable block
        into the variable key, the variable value and any remaining comment.

        Args:
            var_line (str): line from the input file to process

        Returns:
            [str,str/float,str]: returns a three element list. The first element
                is the variable key, the second is the variable value as a float
                or string, the third is any comment string remaining.
        """

        extract_var = var_line.strip()
        extract_var = extract_var.replace(self._end_char, "")
        extract_var = extract_var.split(self._comment_char)[0]  # Remove trailing comments should they exist

        var_key = ""
        var_val = ""
        if extract_var and extract_var.find("=") >= 0:
            var_str = extract_var.split("=", 1)[1]
            var_str = var_str.strip()
            try:
                var_val = float(var_str)
                if var_val.is_integer():
                    var_val = int(var_val)
            except ValueError:
                var_val = var_str

            var_key = extract_var.split("=", 1)[0].strip()

        if len(var_line.split(self._comment_char)) > 1:
            com_loc = var_line.find(self._comment_char)
            comment_str = var_line[com_loc + len(self._comment_char) :]
        else:
            comment_str = ""

        return (var_key, var_val, comment_str)


    def read_vars(self) -> None:
        """Reads the variables in the file"""
        for ss in self._input_lines[self._var_start_ind + 1 : self._var_end_ind]:
            [var_key, var_val, _] = self._extract_var_str(ss)
            if len(var_key) != 0:
                self._vars[var_key] = var_val


    def find_vars(self) -> None:
        """Find what lines the variables are defined on."""

        # TODO: this needs to be made more robust to multiple occurences of variable block characters.
        # Also need to handle cases when the start and end block characters are the same

        start_string = self._comment_char + self._var_start_str
        end_string = self._comment_char + self._var_end_str

        start_found = False
        for ii, ll in enumerate(self._input_lines):
            if start_string in ll and (not start_found):
                self._var_start_ind = ii
                start_found = True
            if end_string in ll:
                self._var_end_ind = ii
                break


    def update_vars(self, new_vars: dict) -> None:
        """Updates the variable dictionary that will be written to the input
        file.

        Args:
            new_vars (dict): new variables to be written to the input file.
                The keys must exist within the dictionary of variables
                extracted from the input file. Only the variables to be edited
                need to be present.
        """
        for kk in new_vars:
            if kk in self._vars:
                self._vars[kk] = new_vars[kk]
            else:
                raise KeyError(
                    f"Key {kk} does not exist in the variables found in the input file. "
                    + "Check input file to make sure the variable exists."
                )


    def write_file(self, input_write_file: Path) -> None:
        """Write the input file using the current variable dictionary.

        Args:
            input_write_file (str): Path to where the file should be written.
        """
        var_block = self._input_lines[self._var_start_ind + 1 : self._var_end_ind]

        for ii, ll in enumerate(var_block):
            [var_key, _, com_str] = self._extract_var_str(ll)
            if (len(var_key) != 0) and (var_key in self._vars):
                if len(com_str) == 0:
                    var_line = f"{var_key} = {self._vars[var_key]}{self._end_char}\n"
                else:
                    # NOTE: comment string includes the new line character already
                    var_line = f"{var_key} = {self._vars[var_key]}{self._end_char} {self._comment_char}{com_str}"
                line_ind = ii + self._var_start_ind + 1
                self._input_lines[line_ind] = var_line

        with open(input_write_file, "w", encoding="utf-8") as out_file:
            out_file.writelines(self._input_lines)


    def get_vars(self) -> dict:
        """Gets the variables found in the file.

        Returns:
            dict: keys are variable strings and values are variable values.
        """
        return self._vars


    def get_var_keys(self) -> list[str]:
        """Gets a list of variable names found in the input file.

        Returns:
            list[str]: list of variables name as strings
        """
        return list(self._vars.keys())


    def get_input_file(self) -> Path:
        """Gets the path and input file name.

        Returns:
            Path: path and input file name.
        """
        return self._input_file
