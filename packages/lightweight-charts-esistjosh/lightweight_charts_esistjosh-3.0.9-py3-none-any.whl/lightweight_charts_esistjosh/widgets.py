import asyncio
import html
import os 
from .util import parse_event_message
from .abstract import Window, INDEX, AbstractChart

try:
    import wx.html2
except ImportError:
    wx = None

try:
    using_pyside6 = False
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtWebChannel import QWebChannel
    from PyQt5.QtCore import QObject, pyqtSlot as Slot, QUrl, QTimer
except ImportError:
    using_pyside6 = True
    try:
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWebChannel import QWebChannel
        from PySide6.QtCore import Qt, QObject, Slot, QUrl, QTimer
    except ImportError:
        try:
            using_pyside6 = False
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            from PyQt6.QtWebChannel import QWebChannel
            from PyQt6.QtCore import QObject, pyqtSlot as Slot, QUrl, QTimer
        except ImportError:
            QWebEngineView = None


if QWebEngineView:
    class Bridge(QObject):
        def __init__(self, chart):
            super().__init__()
            self.win = chart.win

        @Slot(str)
        def callback(self, message):
            emit_callback(self.win, message)

try:
    from streamlit.components.v1 import html as sthtml
except ImportError:
    sthtml = None

try:
    from IPython.display import HTML, display
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="IPython.core.display")
except ImportError:
    HTML = None


def emit_callback(window, string):
    func, args = parse_event_message(window, string)
    if asyncio.iscoroutinefunction(func):
        asyncio.create_task(func(*args))
    else:
        func(*args)


class WxChart(AbstractChart):
    def __init__(
        self,
        parent,
        inner_width: float = 1.0,
        inner_height: float = 1.0,
        scale_candles_only: bool = False,
        toolbox: str = "default",
        defaults: str = '../defaults',
        scripts: str = '../scripts'
    ):
        if wx is None:
            raise ModuleNotFoundError('wx.html2 was not found, and must be installed to use WxChart.')
        self.webview: wx.html2.WebView = wx.html2.WebView.New(parent)
        super().__init__(
            Window(self.webview.RunScript, 'window.wx_msg.postMessage.bind(window.wx_msg)'),
            inner_width,
            inner_height,
            scale_candles_only,
            toolbox,
            defaults=defaults,
            scripts=scripts
        )

        self.webview.Bind(
            wx.html2.EVT_WEBVIEW_LOADED,
            lambda e: wx.CallLater(500, self.win.on_js_load)
        )
        self.webview.Bind(
            wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED,
            lambda e: emit_callback(self.win, e.GetString())
        )
        self.webview.AddScriptMessageHandler('wx_msg')
        self.webview.LoadURL("file://" + INDEX)

    def get_webview(self):
        return self.webview

class QtChart(AbstractChart):
    def __init__(
        self,
        widget=None,
        inner_width: float = 1.0,
        inner_height: float = 1.0,
        scale_candles_only: bool = False,
        toolbox: str = "default",
        defaults: str = '../defaults',
        scripts: str = '../scripts'
    ):
        if QWebEngineView is None:
            raise ModuleNotFoundError('QWebEngineView was not found, and must be installed to use QtChart.')
        self.webview = QWebEngineView(widget)
        super().__init__(
            Window(self.webview.page().runJavaScript, 'window.pythonObject.callback'),
            inner_width,
            inner_height,
            scale_candles_only,
            toolbox,
            autosize=True ,
            defaults=defaults,
            scripts=scripts
        )

        # Load all necessary files inline, just like in StaticLWC
        js_dir = os.path.dirname(INDEX)
        with open(os.path.join(js_dir, 'styles.css'), 'r') as f:
            css = f.read()
        with open(os.path.join(js_dir, 'lightweight-charts.js'), 'r') as f:
            lwc = f.read()
        with open(os.path.join(js_dir, 'bundle.js'), 'r') as f:
            bundle_js = f.read()

        # Build a custom HTML that ensures the correct load order
        custom_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chart</title>
    <style>{css}</style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div id="container"></div>
    
    <script>
    console.log("Loading lightweight-charts...");
    </script>
    
    <script>{lwc}</script>
    
    <script>
    console.log("Loading Monaco/require.js workaround...");
    // Simulate the RequireJS environment so that bundle.js works
    window.monaco = {{}};
    window.require = {{
        config: function() {{}},
    }};
    window.require.defined = function() {{ return true; }};
    window.define = function(a, b, c) {{
        if (typeof c === 'function') window._bundleExports = c();
    }};
    </script>
    
    <script>{bundle_js}</script>
    
    <script>
    console.log("Initializing Lib from bundle.js...");
    // Ensure that Lib is defined globally
    window.Lib = window.Lib || window._bundleExports;
    console.log("Lib defined:", typeof Lib !== 'undefined');
    window.LibReady = true;
    </script>
</body>
</html>"""

        # Set up the WebChannel bridge between JS and Python
        self.web_channel = QWebChannel()
        self.bridge = Bridge(self)
        self.web_channel.registerObject('bridge', self.bridge)
        self.webview.page().setWebChannel(self.web_channel)

        # Inject the fully assembled HTML
        self.webview.setHtml(custom_html, QUrl(f"file://{js_dir}/"))

        # After load, attach QWebChannel script
        self.webview.loadFinished.connect(lambda: self.webview.page().runJavaScript('''
            console.log("Page loaded, adding QWebChannel...");
            let scriptElement = document.createElement("script");
            scriptElement.src = 'qrc:///qtwebchannel/qwebchannel.js';
            scriptElement.onload = function() {
                console.log("QWebChannel script loaded");
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.pythonObject = channel.objects.bridge;
                    console.log("QWebChannel initialized successfully");
                });
            };
            document.head.appendChild(scriptElement);
        '''))

        # Give enough time for the JS side to initialize before firing on_js_load
        self.webview.loadFinished.connect(lambda: QTimer.singleShot(1000, self.win.on_js_load))

        if using_pyside6:
            self.webview.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

    def get_webview(self):
        return self.webview

class StaticLWC(AbstractChart):
    def __init__(
        self,
        width=None,
        height=None,
        inner_width=1,
        inner_height=1,
        scale_candles_only: bool = False,
        toolbox: str = "default",
        autosize=True,
        defaults: str = '../defaults',
        scripts: str = '../scripts'
    ):
        # Inline CSS & JS into a single HTML payload
        with open(INDEX.replace("index.html", 'styles.css'), 'r') as f:
            css = f.read()
        with open(INDEX.replace("index.html", 'bundle.js'), 'r') as f:
            js = f.read()
        with open(INDEX.replace("index.html", 'lightweight-charts.js'), 'r') as f:
            lwc = f.read()
        with open(INDEX, 'r') as f:
            self._html = (
                f.read()
                .replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>")
                .replace(' src="./lightweight-charts.js">', f'>{lwc}')
                .replace(' src="./bundle.js">', f'>{js}')
                .replace('</body>\n</html>', '<script>')
            )

        super().__init__(
            Window(run_script=self.run_script),
            inner_width,
            inner_height,
            scale_candles_only,
            toolbox,
            autosize,
            defaults=defaults,
            scripts=scripts
        )
        self.width = width
        self.height = height

    def run_script(self, script: str, run_last: bool = False):
        if run_last:
            self.win.final_scripts.append(script)
        else:
            self._html += '\n' + script

    def load(self):
        if self.win.loaded:
            return
        self.win.loaded = True
        for script in self.win.final_scripts:
            self._html += '\n' + script
        self._load()

    def _load(self):
        pass

class StreamlitChart(StaticLWC):
    def __init__(
        self,
        width=None,
        height=None,
        inner_width=1,
        inner_height=1,
        scale_candles_only: bool = False,
        toolbox: str = "default",
        defaults: str = '../defaults',
        scripts: str = '../scripts'
    ):
        super().__init__(width, height, inner_width, inner_height,
                         scale_candles_only, toolbox, autosize=False,
                         defaults=defaults, scripts=scripts)

    def _load(self):
        if sthtml is None:
            raise ModuleNotFoundError(
                'streamlit.components.v1.html was not found, and must be installed to use StreamlitChart.'
            )
        sthtml(f'{self._html}</script></body></html>', width=self.width, height=self.height)

class JupyterChart(StaticLWC):
    def __init__(
        self,
        width: int = 800,
        height: int = 350,
        inner_width=1,
        inner_height=1,
        scale_candles_only: bool = False,
        toolbox: str = "default",
        defaults: str = '../defaults',
        scripts: str = '../scripts'
    ):
        super().__init__(width, height, inner_width, inner_height,
                         scale_candles_only, toolbox, autosize=False,
                         defaults=defaults, scripts=scripts)

        # Ensure container styling fits the notebook
        self.run_script(f'''
            for (var i = 0; i < document.getElementsByClassName("tv-lightweight-charts").length; i++) {{
                var element = document.getElementsByClassName("tv-lightweight-charts")[i];
                element.style.overflow = "visible"
            }}
            document.getElementById('container').style.overflow = 'hidden'
            document.getElementById('container').style.borderRadius = '10px'
            document.getElementById('container').style.width = '{self.width}px'
            document.getElementById('container').style.height = '100%'
        ''')
        self.run_script(f'{self.id}.chart.resize({width}, {height})')

    def _load(self):
        if HTML is None:
            raise ModuleNotFoundError(
                'IPython.display.HTML was not found, and must be installed to use JupyterChart.'
            )
        html_code = html.escape(f"{self._html}</script></body></html>")
        iframe = (
            f'<iframe width="{self.width}" height="{self.height}" '
            f'frameBorder="0" srcdoc="{html_code}"></iframe>'
        )
        display(HTML(iframe))
