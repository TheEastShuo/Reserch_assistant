import os

from PySide6.QtWidgets import QDialog, QFileDialog, QPushButton, QGroupBox, QGridLayout, QLineEdit, QLabel, \
    QCheckBox, QWidget, QRadioButton, QButtonGroup, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog

from Capacity_efficency_curve import Process_Cap_Eff
from Cyclic_Voltammetry_curve import Process_CV
from Voltage_capacity_curve import Process_Cap_Volt


class Status:
    def __init__(self):
        # 初始化读取ui 文件
        self.ui = QUiLoader().load(r'科研小助手_主窗口.ui')

        # 浏览导出文件路径按钮，连接逻辑函数
        self.ui.PButton_OutRead.clicked.connect(lambda: self.OutPath(self.ui.LEdit_OutPath))

        # 浏览导入文件路径按钮，连接逻辑函数
        self.ui.PButton_Cap_Volt_SrcRead.clicked.connect(lambda:self.ReadSrc(self.ui.LEdit_Cap_Volt_SrcPath,
                                                                             self.ui.buttonGroup.checkedButton()))
        self.ui.PButton_Cap_Eff_SrcRead.clicked.connect(lambda: self.ReadSrc(self.ui.LEdit_Cap_Eff_SrcPath,
                                                                             self.ui.buttonGroup_2.checkedButton()))
        self.ui.PButton_CV_SrcRead.clicked.connect(lambda: self.ReadSrc(self.ui.LEdit_CV_SrcPath,
                                                                        self.ui.buttonGroup_3.checkedButton()))

        # 开始处理按钮，连接逻辑函数
        self.ui.PButton_Cap_Volt_Start.clicked.connect(lambda: Process_Cap_Volt(self.ui.LEdit_Cap_Volt_SrcPath.text(),
                                                                                self.ui.LEdit_OutPath.text()))
        self.ui.PButton_Cap_Eff_Start.clicked.connect(lambda: Process_Cap_Eff(self.ui.LEdit_Cap_Eff_SrcPath.text(),
                                                                              self.ui.LEdit_OutPath.text()))
        self.ui.PButton_CV_Start.clicked.connect(lambda: Process_CV(self.ui.LEdit_CV_SrcPath.text(),
                                                                    self.ui.LEdit_OutPath.text()))


        # 数据处理完毕后，输出信息
        self.ui.PButton_Cap_Volt_Start.clicked.connect(lambda: self.Finished(self.ui.LEdit_Cap_Volt_SrcPath.text(),
                                                                                self.ui.LEdit_OutPath.text()))
        self.ui.PButton_Cap_Eff_Start.clicked.connect(lambda: self.Finished(self.ui.LEdit_Cap_Eff_SrcPath.text(),
                                                                              self.ui.LEdit_OutPath.text()))
        self.ui.PButton_CV_Start.clicked.connect(lambda: self.Finished(self.ui.LEdit_CV_SrcPath.text(),
                                                                    self.ui.LEdit_OutPath.text()))
    def ReadSrc(self, LEdit: QLineEdit, Type: QRadioButton):
        LEdit.setText(
            QFileDialog.getOpenFileName(self.ui, '选择数据源文件', filter='数据类型 (*{})'.format(Type.text()))[0])

    def OutPath(self, LEdit: QLineEdit):
        # 获取导出的目录
        LEdit.setText(QFileDialog.getExistingDirectory(self.ui, '选择文件导出目录'))

    def Finished(self, src, out):
        QMessageBox.about(self.ui, '提示', '数据已处理并导出！')
        # 如果“文件导出后打开”被勾选，则自动打开文件
        if self.ui.CBox_OpenOrNot.isChecked() == True:
            os.system(out + r"\out_" + os.path.basename(src))


