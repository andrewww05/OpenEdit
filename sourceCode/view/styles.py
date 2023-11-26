window_style = '''
    background-color: #3e3e42;
    padding: 0;
'''

button_style ='''
        QPushButton{
            background-color: #252526;
            color: white;
            border: none;
            padding: 15px 32px;
            height: 40px;
            text-align: center;
            text-decoration: none;
            font-weight: 400;
            font-size: 16px;
            margin: 2px;
        }
        QPushButton:hover {
            background-color: white;
            color: #8e8e92;
        }
        '''

button_style_secondary = '''
        QPushButton{
            background-color: #007acc;
            color: white;
            border: none;
            padding: 15px 32px;
            height: 40px;
            text-align: center;
            text-decoration: none;
            font-weight: 400;
            font-size: 16px;
            margin: 2px;
        }
        QPushButton:hover {
            background-color: white;
            color: #8e8e92;
        }
        '''

actions_menu_style = '''
        QWidget{
            background-color: '#3e3e42';
        }
        '''

slider_style = """
            QSlider::groove:horizontal {
                height: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #B1B1B1, stop:1 #c4c4c4);
            }

            QSlider::handle:horizontal {
                background-color: #007acc;
                width: 18px;
                margin-top: -3px;
                margin-bottom: -3px;
            }
            """

slider_groupbox = """
    QGroupBox {
        border: 0;
    }
    QLabel {
        color: white;
        font-size: 16px;
        font-weight: 200;
        margin: 0;
    }
"""

slider_label = """
    color: white;
    font-size: 16px;
"""

checkbox_label = """
    color: white;
    font-size: 16px;
"""

checkbox_style = """
    QCheckBox {
        color: white;
        font-size: 16px;
        margin-left: 70px;
    }
    
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 6px;
    }
    
    QCheckBox::indicator:unchecked {
        background-color: #3e3e42;
        border: 2px solid #8e8e92;
    }
    
    QCheckBox::indicator:checked {
        background-color: #007acc;
        border: 2px solid #007acc;
    }
    
    QCheckBox::indicator:unchecked:hover,
    QCheckBox::indicator:checked:hover {
        background-color: #005a7f;
        border: 2px solid #005a7f; 
    }
    
    QCheckBox::indicator:unchecked:pressed,
    QCheckBox::indicator:checked:pressed {
        background-color: #007acc;
        border: 2px solid #007acc;
    }
"""