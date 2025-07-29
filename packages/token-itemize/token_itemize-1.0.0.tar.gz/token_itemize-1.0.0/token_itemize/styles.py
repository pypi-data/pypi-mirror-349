# token_itemize/styles.py
from PyQt5.QtGui import QColor, QFont

class DesignTokens:
    SPACINGS = {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px'
    }
    
    TYPOGRAPHY = {
        'font_family': 'Segoe UI, system-ui',
        'base_size': '14px',
        'title1': QFont('Segoe UI', 24, QFont.Bold),
        'title2': QFont('Segoe UI', 18, QFont.Medium),
        'body': QFont('Segoe UI', 14),
        'caption': QFont('Segoe UI', 12)
    }

class LightTheme:
    COLORS = {
        'primary': QColor('#2962FF'),
        'secondary': QColor('#03DAC5'),
        'surface': QColor('#FFFFFF'),
        'background': QColor('#F8F9FA'),
        'on_primary': QColor('#FFFFFF'),
        'on_surface': QColor('#212121'),
        'error': QColor('#B00020'),
        'hover': QColor('#00000015'),
        'focus': QColor('#2962FF20')
    }

class DarkTheme:
    COLORS = {
        'primary': QColor('#BB86FC'),
        'secondary': QColor('#03DAC6'),
        'surface': QColor('#2D2D2D'),
        'background': QColor('#121212'),
        'on_primary': QColor('#000000'),
        'on_surface': QColor('#FFFFFF'),
        'error': QColor('#CF6679'),
        'hover': QColor('#FFFFFF15'),
        'focus': QColor('#BB86FC20')
    }

class StyleHelper:
    @staticmethod
    def apply_theme(app, dark_mode=False):
        if dark_mode:
            theme = DarkTheme
            neon_border = "#39FF14"  # Neon green for dark mode checkboxes
        else:
            theme = LightTheme
            neon_border = theme.COLORS['on_surface'].name()

        tokens = DesignTokens()
        
        style = f"""
            QWidget {{
                background-color: {theme.COLORS['background'].name()};
                color: {theme.COLORS['on_surface'].name()};
                font-family: {tokens.TYPOGRAPHY['font_family']};
                font-size: {tokens.TYPOGRAPHY['base_size']};
            }}
            
            QPushButton {{
                background-color: {theme.COLORS['primary'].name()};
                color: {theme.COLORS['on_primary'].name()};
                border-radius: 4px;
                padding: {tokens.SPACINGS['sm']} {tokens.SPACINGS['md']};
                min-width: 96px;
            }}
            
            QPushButton:hover {{
                background-color: {theme.COLORS['primary'].darker(110).name()};
            }}
            
            QPushButton:pressed {{
                background-color: {theme.COLORS['primary'].darker(120).name()};
            }}
            
            QPushButton:disabled {{
                background-color: {theme.COLORS['primary'].lighter(120).name()};
                color: {theme.COLORS['on_primary'].darker(100).name()};
            }}
            
            QLineEdit, QComboBox {{
                background-color: {theme.COLORS['surface'].name()};
                border: 1px solid {theme.COLORS['on_surface'].name()}30;
                padding: {tokens.SPACINGS['sm']};
            }}
            
            QTableWidget {{
                gridline-color: {theme.COLORS['on_surface'].name()}30;
                background-color: {theme.COLORS['surface'].name()};
            }}
            
            QHeaderView::section {{
                background-color: {theme.COLORS['surface'].name()};
                color: {theme.COLORS['on_surface'].name()};
            }}
            
            QProgressBar {{
                border: 1px solid {theme.COLORS['on_surface'].name()}30;
                border-radius: 4px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {theme.COLORS['primary'].name()};
            }}
            
            /* Checkboxes: Outline with neon green in dark mode */
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {neon_border};
                border-radius: 3px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {neon_border};
            }}
        """
        app.setStyleSheet(style)
