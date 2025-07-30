from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from boj.core.browser import Browser
from boj.core.error import AuthenticationError, IllegalStatementError, FatalError


class LoginBrowser(Browser):
    def wait_for_login(self):
        while True:
            try:
                if "login" not in self.driver.current_url:
                    break

                element = self.driver.find_element(By.NAME, "auto_login")
                if not element.is_selected():
                    element.click()
                    self.driver.find_element(By.NAME, "login_user_id").click()
                    continue
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                break
            except Exception:
                raise FatalError("login failed")

        try:
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "username")))
        except FatalError as e:
            raise e
        except Exception:
            raise FatalError("failed to identify user")

        token = self.driver.get_cookie("bojautologin")
        if "value" not in token:
            raise FatalError("could not find session token")

        return {"username": element.text, "token": token["value"]}
