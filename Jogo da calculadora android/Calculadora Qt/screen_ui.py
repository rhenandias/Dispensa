# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screen.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(385, 494)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 391, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 320, 361, 51))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.layout_solution = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.layout_solution.setContentsMargins(0, 0, 0, 0)
        self.layout_solution.setObjectName("layout_solution")
        self.label_result = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_result.setObjectName("label_result")
        self.layout_solution.addWidget(self.label_result, 1, 0, 1, 1)
        self.label_solution = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.label_solution.setAlignment(QtCore.Qt.AlignCenter)
        self.label_solution.setObjectName("label_solution")
        self.layout_solution.addWidget(self.label_solution, 0, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(110, 270, 160, 44))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.layout_evaluate_and_clear = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.layout_evaluate_and_clear.setContentsMargins(0, 0, 0, 0)
        self.layout_evaluate_and_clear.setObjectName("layout_evaluate_and_clear")
        self.button_clear = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.button_clear.setObjectName("button_clear")
        self.layout_evaluate_and_clear.addWidget(self.button_clear, 0, 1, 1, 1)
        self.button_evaluate = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.button_evaluate.setObjectName("button_evaluate")
        self.layout_evaluate_and_clear.addWidget(self.button_evaluate, 0, 0, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 140, 163, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.layout_add_operation_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.layout_add_operation_1.setContentsMargins(0, 0, 0, 0)
        self.layout_add_operation_1.setObjectName("layout_add_operation_1")
        self.label_add_operation = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_add_operation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_add_operation.setObjectName("label_add_operation")
        self.layout_add_operation_1.addWidget(self.label_add_operation)
        self.layout_add_operation_2 = QtWidgets.QGridLayout()
        self.layout_add_operation_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout_add_operation_2.setObjectName("layout_add_operation_2")
        self.button_add_operation = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.button_add_operation.setObjectName("button_add_operation")
        self.layout_add_operation_2.addWidget(self.button_add_operation, 0, 1, 1, 1)
        self.input_operation = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_operation.setObjectName("input_operation")
        self.layout_add_operation_2.addWidget(self.input_operation, 0, 0, 1, 1)
        self.layout_add_operation_1.addLayout(self.layout_add_operation_2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 210, 361, 51))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.layout_available_operations = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.layout_available_operations.setContentsMargins(0, 0, 0, 0)
        self.layout_available_operations.setObjectName("layout_available_operations")
        self.label_available_operations_title = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_available_operations_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_available_operations_title.setObjectName("label_available_operations_title")
        self.layout_available_operations.addWidget(self.label_available_operations_title)
        self.label_available_operations = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_available_operations.setAlignment(QtCore.Qt.AlignCenter)
        self.label_available_operations.setObjectName("label_available_operations")
        self.layout_available_operations.addWidget(self.label_available_operations)
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(110, 10, 160, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.layout_inputs = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.layout_inputs.setContentsMargins(0, 0, 0, 0)
        self.layout_inputs.setObjectName("layout_inputs")
        self.label_target = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_target.setObjectName("label_target")
        self.layout_inputs.addWidget(self.label_target, 3, 0, 1, 1)
        self.label_start = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_start.setObjectName("label_start")
        self.layout_inputs.addWidget(self.label_start, 5, 0, 1, 1)
        self.label_moves = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_moves.setObjectName("label_moves")
        self.layout_inputs.addWidget(self.label_moves, 4, 0, 1, 1)
        self.label_problem = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_problem.setObjectName("label_problem")
        self.layout_inputs.addWidget(self.label_problem, 1, 0, 1, 1)
        self.input_problem = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.input_problem.setMaximum(200)
        self.input_problem.setObjectName("input_problem")
        self.layout_inputs.addWidget(self.input_problem, 1, 1, 1, 1)
        self.input_target = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.input_target.setMinimum(-9999)
        self.input_target.setMaximum(9999)
        self.input_target.setObjectName("input_target")
        self.layout_inputs.addWidget(self.input_target, 3, 1, 1, 1)
        self.input_moves = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.input_moves.setObjectName("input_moves")
        self.layout_inputs.addWidget(self.input_moves, 4, 1, 1, 1)
        self.input_start = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.input_start.setMinimum(-9999)
        self.input_start.setMaximum(9999)
        self.input_start.setObjectName("input_start")
        self.layout_inputs.addWidget(self.input_start, 5, 1, 1, 1)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 380, 361, 61))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.layout_manual_operation = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.layout_manual_operation.setContentsMargins(0, 0, 0, 0)
        self.layout_manual_operation.setObjectName("layout_manual_operation")
        self.label_manual_operation = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_manual_operation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_manual_operation.setObjectName("label_manual_operation")
        self.layout_manual_operation.addWidget(self.label_manual_operation)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.input_manual_operation = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_manual_operation.sizePolicy().hasHeightForWidth())
        self.input_manual_operation.setSizePolicy(sizePolicy)
        self.input_manual_operation.setFrame(True)
        self.input_manual_operation.setAlignment(QtCore.Qt.AlignCenter)
        self.input_manual_operation.setObjectName("input_manual_operation")
        self.gridLayout.addWidget(self.input_manual_operation, 0, 3, 1, 1)
        self.input_total = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.input_total.setMinimum(-9999)
        self.input_total.setMaximum(9999)
        self.input_total.setObjectName("input_total")
        self.gridLayout.addWidget(self.input_total, 0, 1, 1, 1)
        self.label_total = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_total.setAlignment(QtCore.Qt.AlignCenter)
        self.label_total.setObjectName("label_total")
        self.gridLayout.addWidget(self.label_total, 0, 0, 1, 1)
        self.label_operation = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_operation.setAlignment(QtCore.Qt.AlignCenter)
        self.label_operation.setObjectName("label_operation")
        self.gridLayout.addWidget(self.label_operation, 0, 2, 1, 1)
        self.button_evaluate_manual_operation = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_evaluate_manual_operation.sizePolicy().hasHeightForWidth())
        self.button_evaluate_manual_operation.setSizePolicy(sizePolicy)
        self.button_evaluate_manual_operation.setObjectName("button_evaluate_manual_operation")
        self.gridLayout.addWidget(self.button_evaluate_manual_operation, 0, 4, 1, 1)
        self.layout_manual_operation.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(110, 20, 160, 152))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.layout_inputs_2 = QtWidgets.QGridLayout()
        self.layout_inputs_2.setObjectName("layout_inputs_2")
        self.label_target_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_target_2.setObjectName("label_target_2")
        self.layout_inputs_2.addWidget(self.label_target_2, 3, 0, 1, 1)
        self.label_start_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_start_2.setObjectName("label_start_2")
        self.layout_inputs_2.addWidget(self.label_start_2, 5, 0, 1, 1)
        self.label_moves_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_moves_2.setObjectName("label_moves_2")
        self.layout_inputs_2.addWidget(self.label_moves_2, 4, 0, 1, 1)
        self.label_problem_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.label_problem_2.setObjectName("label_problem_2")
        self.layout_inputs_2.addWidget(self.label_problem_2, 1, 0, 1, 1)
        self.input_new_problem = QtWidgets.QSpinBox(self.verticalLayoutWidget_4)
        self.input_new_problem.setMaximum(200)
        self.input_new_problem.setObjectName("input_new_problem")
        self.layout_inputs_2.addWidget(self.input_new_problem, 1, 1, 1, 1)
        self.input_new_target = QtWidgets.QSpinBox(self.verticalLayoutWidget_4)
        self.input_new_target.setMinimum(-9999)
        self.input_new_target.setMaximum(9999)
        self.input_new_target.setObjectName("input_new_target")
        self.layout_inputs_2.addWidget(self.input_new_target, 3, 1, 1, 1)
        self.input_new_moves = QtWidgets.QSpinBox(self.verticalLayoutWidget_4)
        self.input_new_moves.setObjectName("input_new_moves")
        self.layout_inputs_2.addWidget(self.input_new_moves, 4, 1, 1, 1)
        self.input_new_start = QtWidgets.QSpinBox(self.verticalLayoutWidget_4)
        self.input_new_start.setMinimum(-9999)
        self.input_new_start.setMaximum(9999)
        self.input_new_start.setObjectName("input_new_start")
        self.layout_inputs_2.addWidget(self.input_new_start, 5, 1, 1, 1)
        self.verticalLayout.addLayout(self.layout_inputs_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_append_problem = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.input_append_problem.setObjectName("input_append_problem")
        self.horizontalLayout.addWidget(self.input_append_problem)
        self.input_clear_append_problem = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.input_clear_append_problem.setObjectName("input_clear_append_problem")
        self.horizontalLayout.addWidget(self.input_clear_append_problem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(110, 190, 172, 171))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.layout_inputs_3 = QtWidgets.QGridLayout()
        self.layout_inputs_3.setObjectName("layout_inputs_3")
        self.label_target_3 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_target_3.setObjectName("label_target_3")
        self.layout_inputs_3.addWidget(self.label_target_3, 3, 0, 1, 1)
        self.label_start_3 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_start_3.setObjectName("label_start_3")
        self.layout_inputs_3.addWidget(self.label_start_3, 5, 0, 1, 1)
        self.label_moves_3 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_moves_3.setObjectName("label_moves_3")
        self.layout_inputs_3.addWidget(self.label_moves_3, 4, 0, 1, 1)
        self.label_problem_3 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_problem_3.setObjectName("label_problem_3")
        self.layout_inputs_3.addWidget(self.label_problem_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setText("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.layout_inputs_3.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setText("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.layout_inputs_3.addWidget(self.label_5, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_6.setAutoFillBackground(False)
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setText("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.layout_inputs_3.addWidget(self.label_6, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_7.setAutoFillBackground(False)
        self.label_7.setFrameShape(QtWidgets.QFrame.Box)
        self.label_7.setText("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.layout_inputs_3.addWidget(self.label_7, 5, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.layout_inputs_3)
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(110, 370, 170, 80))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_6)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.gridLayoutWidget_6)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 2, 1, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculator: The Game Solver"))
        self.label_result.setText(_translate("MainWindow", "[   ]"))
        self.label_solution.setText(_translate("MainWindow", "Solução"))
        self.button_clear.setText(_translate("MainWindow", "Limpar"))
        self.button_evaluate.setText(_translate("MainWindow", "Validar"))
        self.label_add_operation.setText(_translate("MainWindow", "Adicionar Operações"))
        self.button_add_operation.setText(_translate("MainWindow", "Add"))
        self.label_available_operations_title.setText(_translate("MainWindow", "Operações Disponíveis"))
        self.label_available_operations.setText(_translate("MainWindow", "[   ]"))
        self.label_target.setText(_translate("MainWindow", "Objetivo"))
        self.label_start.setText(_translate("MainWindow", "Inicio"))
        self.label_moves.setText(_translate("MainWindow", "Movimentos"))
        self.label_problem.setText(_translate("MainWindow", "Problema"))
        self.label_manual_operation.setText(_translate("MainWindow", "Operação Manual"))
        self.label_total.setText(_translate("MainWindow", "Total"))
        self.label_operation.setText(_translate("MainWindow", "Operação"))
        self.button_evaluate_manual_operation.setText(_translate("MainWindow", "Validar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Calculadora"))
        self.label.setText(_translate("MainWindow", "Registrar Novo Problema"))
        self.label_target_2.setText(_translate("MainWindow", "Objetivo"))
        self.label_start_2.setText(_translate("MainWindow", "Inicio"))
        self.label_moves_2.setText(_translate("MainWindow", "Movimentos"))
        self.label_problem_2.setText(_translate("MainWindow", "Problema"))
        self.input_append_problem.setText(_translate("MainWindow", "Registrar"))
        self.input_clear_append_problem.setText(_translate("MainWindow", "Limpar"))
        self.label_2.setText(_translate("MainWindow", "Visualizar Problema"))
        self.label_target_3.setText(_translate("MainWindow", "Objetivo"))
        self.label_start_3.setText(_translate("MainWindow", "Inicio"))
        self.label_moves_3.setText(_translate("MainWindow", "Movimentos"))
        self.label_problem_3.setText(_translate("MainWindow", "Problema"))
        self.label_3.setText(_translate("MainWindow", "Problema"))
        self.pushButton.setText(_translate("MainWindow", "Go"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Problemas"))
