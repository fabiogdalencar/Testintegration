import pytest
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

global driver
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name=request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "IE":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.close()


'''@pytest.fixture(scope="class")
def driver_init_1(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    request.cls.driver = driver
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    yield
    driver.close()


@pytest.fixture(scope="class")
def driver_init_2(request):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    request.cls.driver = driver
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.maximize_window()
    yield
    driver.close()'''




@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))

        report.extra = extra


def _capture_screenshot(name):
        driver.save_screenshot(name)

