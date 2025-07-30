"""Chrome browser driver implementation."""
import logging
import os
import platform
import shutil
import struct
import sys
import zipfile
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Type, TypeVar, Callable

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.common.exceptions import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

from ..base import BaseBrowser
from ..driver_config import DriverConfig
from ..exceptions import (
    BrowserError,
    BrowserNotInitializedError,
    NavigationError,
    ScreenshotError,
    ElementNotFoundError,
    ElementNotInteractableError,
    TimeoutError as BrowserTimeoutError
)
from ..features.element import ElementHelper
from ..features.navigation import NavigationMixin
from ..features.screenshot import ScreenshotHelper
from . import register_driver, BaseBrowserDriver

# Type variable for generic typing
T = TypeVar('T')

# Type alias for WebDriver
WebDriver = ChromeWebDriver


@register_driver("chrome")
class ChromeDriver(BaseBrowserDriver, NavigationMixin, ElementHelper, ScreenshotHelper):
    """Chrome browser driver implementation.
    
    This class provides a high-level interface for browser automation with Chrome,
    including navigation, element interaction, and screenshot capabilities.
    """
    
    def __init__(self, config: Any, logger: Optional[logging.Logger] = None):
        """Initialize the Chrome browser.
        
        Args:
            config: Configuration object containing browser settings
            logger: Optional logger instance for logging
        """
        super().__init__(config, logger)
        self.driver: Optional[WebDriver] = None
        self._service: Optional[ChromeService] = None
        self._options: Optional[ChromeOptions] = None
        self._setup_options()
    
    @classmethod
    def get_name(cls) -> str:
        """Get the name of the browser driver.
        
        Returns:
            str: The name of the browser ("chrome")
        """
        return "chrome"
    
    def _setup_options(self) -> None:
        """Set up Chrome options based on configuration."""
        self._options = ChromeOptions()
        
        # Default Chrome arguments for better stability and to suppress warnings
        default_args = [
            '--disable-gpu',  # Disable GPU hardware acceleration
            '--log-level=3',  # Suppress most console logs
            '--no-sandbox',
            '--disable-dev-shm-usage',  # Overcome limited resource problems
            '--disable-software-rasterizer',
            '--disable-extensions',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-browser-side-navigation',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-blink-features=AutomationControlled',
        ]
        
        # Add default arguments if not already specified in config
        chrome_args = getattr(self.config, 'chrome_args', [])
        for arg in default_args + chrome_args:
            if arg.split('=')[0] not in [a.split('=')[0] for a in self._options.arguments]:
                self._options.add_argument(arg)
        
        # Add experimental options if provided
        experimental_options = getattr(self.config, 'experimental_options', {})
        for key, value in experimental_options.items():
            self._options.add_experimental_option(key, value)
        
        # Set window size if specified
        if hasattr(self.config, 'window_size') and self.config.window_size:
            width, height = self.config.window_size
            self._options.add_argument(f'--window-size={width},{height}')
        
        # Disable GPU-related features that might cause warnings
        self._options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self._options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    def navigate_to(self, url: str, wait_time: Optional[float] = None) -> bool:
        """Navigate to the specified URL.
        
        Args:
            url: The URL to navigate to
            wait_time: Optional time to wait for page load
            
        Returns:
            bool: True if navigation was successful
        """
        if not self.driver:
            raise BrowserNotInitializedError("Browser is not initialized. Call start() first.")
        
        try:
            self.driver.get(url)
            if wait_time:
                time.sleep(wait_time)
            return True
        except Exception as e:
            self._logger.error(f"Failed to navigate to {url}: {e}")
            raise NavigationError(f"Failed to navigate to {url}: {e}") from e
    
    def get_page_source(self) -> str:
        """Get the current page source.
        
        Returns:
            str: The page source HTML
        """
        if not self.driver:
            raise BrowserNotInitializedError("Browser is not initialized. Call start() first.")
        return self.driver.page_source
    
    def get_current_url(self) -> str:
        """Get the current URL.
        
        Returns:
            str: The current URL
        """
        if not self.driver:
            raise BrowserNotInitializedError("Browser is not initialized. Call start() first.")
        return self.driver.current_url
    
    def take_screenshot(self, file_path: str, full_page: bool = False) -> bool:
        """Take a screenshot of the current page.
        
        Args:
            file_path: Path to save the screenshot
            full_page: If True, capture the full page (not supported in all browsers)
            
        Returns:
            bool: True if screenshot was successful
        """
        if not self.driver:
            raise BrowserNotInitializedError("Browser is not initialized. Call start() first.")
        
        try:
            self.driver.save_screenshot(file_path)
            return True
        except Exception as e:
            self._logger.error(f"Failed to take screenshot: {e}")
            raise ScreenshotError(f"Failed to take screenshot: {e}") from e
    
    def _create_service(self) -> ChromeService:
        """Create and configure the Chrome service.
        
        Returns:
            ChromeService: Configured Chrome service instance
        """
        driver_config = getattr(self.config, 'driver_config', {})
        
        # Set up service arguments
        service_args = getattr(driver_config, 'service_args', [])
        log_path = getattr(driver_config, 'service_log_path', None)
        
        # Get the driver path, use ChromeDriverManager if not provided
        driver_path = None
        if hasattr(driver_config, 'driver_path') and driver_config.driver_path:
            driver_path = driver_config.driver_path
        else:
            # Use ChromeDriverManager to handle driver installation
            driver_path = ChromeDriverManager().install()
        
        # Create service with configured options
        service = ChromeService(
            executable_path=driver_path,
            service_args=service_args,
            log_path=log_path
        )
        
        return service
    
    def start(self) -> None:
        """Start the Chrome browser."""
        if self.driver is not None:
            self.logger.warning("Browser is already running")
            return
        
        try:
            # Set up Chrome service and options
            self._service = self._create_service()
            
            # Initialize Chrome WebDriver
            self.driver = webdriver.Chrome(
                service=self._service,
                options=self._options
            )
            
            # Configure timeouts
            if hasattr(self.config, 'implicit_wait'):
                self.driver.implicitly_wait(self.config.implicit_wait)
                
            if hasattr(self.config, 'page_load_timeout'):
                self.driver.set_page_load_timeout(self.config.page_load_timeout)
                
            if hasattr(self.config, 'script_timeout'):
                self.driver.set_script_timeout(self.config.script_timeout)
                
            self.logger.info("Chrome browser started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start Chrome browser: {e}")
            self._cleanup_resources()
            raise BrowserError(f"Failed to start Chrome browser: {e}") from e
            
    def _cleanup_resources(self) -> None:
        """Clean up any resources used by the browser."""
        try:
            if self._service:
                self._service.stop()
                self._service = None
        except Exception as e:
            self.logger.warning(f"Error cleaning up Chrome service: {e}")
    
    def stop(self) -> None:
        """Stop the Chrome browser and clean up resources."""
        if self.driver is None:
            return
            
        try:
            self.logger.info("Stopping Chrome browser...")
            self.driver.quit()
            self.logger.info("Chrome browser stopped")
        except Exception as e:
            self.logger.error(f"Error stopping Chrome browser: {e}")
            raise
        finally:
            self.driver = None
            self._cleanup_resources()
    
    def is_running(self) -> bool:
        """Check if the browser is running.
        
        Returns:
            bool: True if the browser is running, False otherwise
        """
        try:
            # Try to get the current URL to check if the browser is still responsive
            if self.driver is None:
                return False
                
            # Check if the browser is still responsive
            _ = self.driver.current_url
            return True
            
        except Exception as e:
            self._logger.debug(f"Browser is not running: {e}")
            return False
            
    def start(self) -> None:
        """Start the Chrome browser."""
        if self.driver is not None:
            self._logger.warning("Browser is already running")
            return
        
        try:
            # Set up Chrome service and options
            self._service = self._create_service()
            
            # Initialize Chrome WebDriver
            self.driver = webdriver.Chrome(
                service=self._service,
                options=self._options
            )
            
            # Configure timeouts
            if hasattr(self.config, 'implicit_wait'):
                self.driver.implicitly_wait(self.config.implicit_wait)
                
            if hasattr(self.config, 'page_load_timeout'):
                self.driver.set_page_load_timeout(self.config.page_load_timeout)
                
            if hasattr(self.config, 'script_timeout'):
                self.driver.set_script_timeout(self.config.script_timeout)
                
            self._logger.info("Chrome browser started successfully")
            
        except Exception as e:
            self._logger.error(f"Failed to start Chrome browser: {e}")
            self._cleanup_resources()
            raise BrowserError(f"Failed to start Chrome browser: {e}") from e
            
    def stop(self) -> None:
        """Stop the Chrome browser and clean up resources."""
        if self.driver is None:
            self._logger.warning("Browser is not running")
            return
            
        try:
            self._logger.info("Stopping Chrome browser...")
            self.driver.quit()
            self._logger.info("Chrome browser stopped")
        except Exception as e:
            self._logger.error(f"Error stopping Chrome browser: {e}")
            raise
        finally:
            self.driver = None
            self._cleanup_resources()
            
    def _cleanup_resources(self) -> None:
        """Clean up any resources used by the browser."""
        if self._service is not None:
            try:
                self._service.stop()
            except Exception as e:
                self._logger.error(f"Error stopping Chrome service: {e}")
            finally:
                self._service = None
            
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
    
    def __getattr__(self, name):
        """Delegate attribute access to the underlying driver."""
        if self.driver is None:
            raise BrowserNotInitializedError(
                "Browser driver not initialized. Call start() first."
            )
        return getattr(self.driver, name)
    
    @property
    def current_url(self) -> str:
        """Get the current URL."""
        if self.driver is None:
            raise BrowserNotInitializedError("Browser is not running")
        return self.driver.current_url
    
    @property
    def title(self) -> str:
        """Get the current page title."""
        if self.driver is None:
            raise BrowserNotInitializedError("Browser is not running")
        return self.driver.title
    
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript in the current browser context."""
        if self.driver is None:
            raise BrowserNotInitializedError("Browser is not running")
        return self.driver.execute_script(script, *args)
    
    def get(self, url: str) -> None:
        """Navigate to the specified URL."""
        if self.driver is None:
            raise BrowserNotInitializedError("Browser is not running")
        try:
            self.driver.get(url)
            self.logger.debug(f"Navigated to: {url}")
        except TimeoutException as e:
            error_msg = f"Timeout while navigating to {url}"
            self.logger.error(error_msg)
            raise BrowserTimeoutError(error_msg) from e
        except WebDriverException as e:
            error_msg = f"Failed to navigate to {url}: {str(e)}"
            self.logger.error(error_msg)
            raise NavigationError(error_msg) from e
