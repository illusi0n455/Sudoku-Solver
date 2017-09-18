import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_sudoku_solver import Ui_Dialog
import sudoku_solver


class MySudokuSolver(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)

        # Connect buttons with a custom functions
        self.btnSolve.clicked.connect(self.solve_sudoku)
        self.btnClear.clicked.connect(self.clear)

    def solve_sudoku(self):
        try:
            self.display_in_text_browser(sudoku_solver.solve(self.get_sudoku()))
        except:
            self.textBrowser.append("Не можу знайти розв’язок. Перевірте введені данні")

    def display_in_text_browser(self, values):
        output = '----------------------'+'\n'
        width = 1 + max(len(values[s]) for s in sudoku_solver.squares)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in sudoku_solver.rows:
            output += ''.join([values[r + c].center(width) + ('|' if c in '36' else '')
                               for c in sudoku_solver.cols]) + "\n"
            if r in 'CF':
                output += line + "\n"
        output += ('----------------------'+'\n')
        self.textBrowser.append(output)

    def clear(self):
        self.textBrowser.clear()
        for i in range(1, 82):
            self.get_edit(i).clear()

    def get_sudoku(self):
        sudoku = ''
        allowed = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(1, 82):
            val = str(self.get_edit(i).toPlainText())
            if val in allowed:
                sudoku += val
            else:
                sudoku += '0'
        return sudoku

    def get_edit(self, int):
        return eval('self.textEdit_{}'.format(int))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = MySudokuSolver(dialog)
    dialog.show()
    sys.exit(app.exec_())
