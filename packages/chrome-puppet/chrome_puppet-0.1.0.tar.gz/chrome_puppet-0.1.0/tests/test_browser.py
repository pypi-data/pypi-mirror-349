"""Tests for the Chrome browser implementation."""
import os
import sys
import time
import pytest
from pathlib import Path
from typing import Generator, TYPE_CHECKING
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Import core module for lazy imports
import core

# Import base test class with a try-except to handle circular imports
try:
    from tests.base_test import BaseTest
except ImportError:
    # This is a workaround for circular imports
    BaseTest = object  # type: ignore

# Lazy imports
def get_chrome_config():
    """Get the ChromeConfig class with lazy import."""
    if core.ChromeConfig is None:
        core._import_config()
    return core.ChromeConfig

# Import exceptions with lazy loading
try:
    from core.browser.exceptions import (
        BrowserError,
        NavigationError,
        ElementNotFoundError,
        ElementNotInteractableError,
        TimeoutError
    )
except ImportError:
    # This is a workaround for circular imports
    BrowserError = Exception
    NavigationError = Exception
    ElementNotFoundError = Exception
    ElementNotInteractableError = Exception
    TimeoutError = Exception

# Mark all tests in this module as browser tests
pytestmark = [pytest.mark.browser, pytest.mark.driver]

class TestChromeDriver(BaseTest):
    """Test cases for ChromeDriver class."""
    
    def test_browser_initialization(self, browser):
        """Test that the browser initializes correctly."""
        # Check that the browser is created
        assert browser.driver is not None
        assert browser.driver.capabilities is not None
        
        # Check that we can navigate to a page
        browser.get("https://httpbin.org/headers")
        assert "httpbin.org" in browser.driver.current_url
        
        # Take a screenshot for verification
        self.take_screenshot(browser, "browser_init_test")
        
        # Check page title
        assert "httpbin" in browser.driver.title.lower()
    
    def test_javascript_execution(self, browser):
        """Test JavaScript execution in the browser."""
        # Execute JavaScript
        user_agent = browser.driver.execute_script("return navigator.userAgent;")
        assert isinstance(user_agent, str)
        assert "Chrome" in user_agent
        
        # Test console.log capture
        browser.driver.execute_script("console.log('Test message from JavaScript');")
    
    def test_window_management(self, browser):
        """Test browser window management."""
        # Test window size
        width = 1024
        height = 768
        browser.driver.set_window_size(width, height)
        
        # Get window size
        window_size = browser.driver.get_window_size()
        assert window_size['width'] == width
        assert window_size['height'] == height
        
        # Test maximize
        browser.driver.maximize_window()
        
    def test_browser_navigation(self, browser):
        """Test that the browser initializes correctly."""
        assert browser.is_running()
        assert browser.driver is not None
        assert "data" in browser.driver.capabilities
    
    def test_navigation(self, browser, test_page_url):
        """Test basic navigation to a URL."""
        browser.get(test_page_url)
        assert "Example Domain" in browser.driver.title
    
    def test_page_source(self, browser, test_page_url):
        """Test retrieving page source."""
        browser.get(test_page_url)
        page_source = browser.get_page_source()
        assert isinstance(page_source, str)
        assert len(page_source) > 0
        assert "Example Domain" in page_source
    
    def test_current_url(self, browser, test_page_url):
        """Test getting the current URL."""
        browser.get(test_page_url)
        current_url = browser.get_current_url()
        assert current_url == test_page_url
    
    def test_take_screenshot(self, browser, test_page_url, tmp_path):
        """Test taking a screenshot."""
        browser.get(test_page_url)
        screenshot_path = tmp_path / "screenshot.png"
        result = browser.screenshot.take_screenshot(str(screenshot_path))
        
        assert result is True
        assert screenshot_path.exists()
        assert screenshot_path.stat().st_size > 0
    
    def test_invalid_url_raises_error(self, browser):
        """Test that navigating to an invalid URL raises an error."""
        with pytest.raises(NavigationError):
            browser.get("http://thisurldoesnotexist.xyz")
    
    def test_browser_restart(self, browser):
        """Test that the browser can be stopped and restarted."""
        # First session
        browser.get("https://example.com")
        assert "Example" in browser.driver.title
        
        # Restart
        browser.stop()
        assert not browser.is_running()
        
        # Second session
        browser.start()
        browser.get("https://example.org")
        assert "Example" in browser.driver.title
    
    def test_custom_user_agent(self, browser):
        """Test custom user agent setting."""
        custom_ua = "ChromePuppet/1.0"  # Just check for the custom part
        full_ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {custom_ua}"
        
        # Create a new browser instance with custom user agent
        from core.browser.chrome import ChromeConfig
        config = ChromeConfig(
            headless=True,
            user_agent=full_ua
        )
        
        # Import ChromePuppet here to avoid circular imports
        from core.browser.puppet import ChromePuppet
        with ChromePuppet(config=config) as custom_browser:
            custom_browser.get("https://httpbin.org/user-agent")
            # The page returns the user agent in the response body
            user_agent = custom_browser.driver.find_element(By.TAG_NAME, "body").text
            # Check if our custom part is in the user agent
            assert custom_ua in user_agent


def test_element_interaction(browser, test_page_with_form):
    """Test various element interactions."""
    browser.get(test_page_with_form)
    
    # Test finding elements
    elements = [
        ("id", "search-input"),
        ("name", "search"),
        ("css", "input[type='text']"),
        ("xpath", "//input[@id='search-input']"),
        ("link text", "Click me"),
        ("partial link text", "Click")
    ]
    
    for by, value in elements:
        element = browser.element.find_element(by, value)
        assert element is not None
        assert element.is_displayed()
    
    # Test sending keys
    search_input = browser.element.find_element("id", "search-input")
    browser.element.send_keys("test search", element=search_input)
    assert search_input.get_attribute("value") == "test search"
    
    # Test clicking
    submit_button = browser.element.find_element("css", "button[type='submit']")
    browser.element.click(submit_button)
    assert "form-submitted" in browser.get_current_url()


def test_screenshot_functionality(browser, tmp_path):
    """Test screenshot capture functionality."""
    # Navigate to a test page
    browser.get("https://httpbin.org/html")
    
    # Take a full page screenshot
    screenshot_path = tmp_path / "full_page.png"
    result = browser.screenshot.take_screenshot(str(screenshot_path))
    
    # Verify the screenshot was created
    assert result is True
    assert screenshot_path.exists()
    assert screenshot_path.stat().st_size > 0
    
    # Test element screenshot
    element = browser.driver.find_element(By.CSS_SELECTOR, "div.ng-scope")
    element_screenshot = element.screenshot_as_png
    element_path = tmp_path / "element.png"
    with open(element_path, 'wb') as f:
        f.write(element_screenshot)
    assert element_path.exists()
    assert element_path.stat().st_size > 0


class TestChromeConfig:
    """Test cases for ChromeConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ChromeConfig()
        assert config.headless is False
        assert config.window_size == (1366, 768)
        assert config.implicit_wait == 30
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ChromeConfig(
            headless=True,
            window_size=(1920, 1080),
            implicit_wait=10,
            chrome_arguments=["--disable-extensions"]
        )
        assert config.headless is True
        assert config.window_size == (1920, 1080)
        assert config.implicit_wait == 10
        assert "--disable-extensions" in config.chrome_arguments

@pytest.mark.slow
def test_parallel_browser_instances():
    """Test that multiple browser instances can run in parallel."""
    config = ChromeConfig(headless=True)
    browsers = []
    
    try:
        # Create multiple browser instances
        for i in range(3):
            browser = ChromeBrowser(config)
            browser.start()
            browser.get(f"https://example.com?test={i}")
            browsers.append(browser)
        
        # Verify all browsers are running
        for i, browser in enumerate(browsers):
            assert browser.is_running()
            assert f"test={i}" in browser.get_current_url()
    finally:
        # Clean up
        for browser in browsers:
            browser.stop()
