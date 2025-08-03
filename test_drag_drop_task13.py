import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Positive scenario
# @pytest.mark.drag_drop_positive
def test_drag_and_drop_positive():
    try:
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('start-maximised')
        options.set_capability('browserName','chrome')
        options.set_capability('platformName', 'Windows 11')
        driver = webdriver.Remote(command_executor="http://192.168.1.9:4444",options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://jqueryui.com/droppable/")
        driver.implicitly_wait(10)

        # Switch to the iframe containing the drag-and-drop elements
        iframe = driver.find_element(By.CLASS_NAME, "demo-frame")
        driver.switch_to.frame(iframe)

        # Locate source and target elements
        drag_location = driver.find_element(By.XPATH,'//div[@id="draggable"]/p')
        drop_location = driver.find_element(By.XPATH,'//div[@id="droppable"]')
        # drop_box=driver.find_element(By.XPATH,'//div[@id="droppable"]/p')

        # Get background color before drop
        color_before = drop_location.value_of_css_property("background-color")

        # Perform drag and drop
        actions = ActionChains(driver)
        actions.move_to_element(drag_location)
        actions.drag_and_drop(drag_location, drop_location).perform()
        time.sleep(10)

        # Get background color after drop
        color_after = drop_location.value_of_css_property("background-color")
        driver.save_screenshot("drag_drop_color_change_positive.png")

        # Assertion
        assert "Dropped!" in drop_location.text,"Mismatch in text displayed"
        print('Drag and Drop performed successfully')
        assert color_before != color_after ,'Drop not happened successfully'
        print(f"Drag and drop successful. Color changed from {color_before} to {color_after}.")

    finally:
        driver.quit()

# negative scenario with source as drop location
# @pytest.mark.drag_drop_negative
def test_drag_and_drop_negative_with_drag_as_drop_location():
    try:
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('start-maximised')
        options.set_capability('browserName','chrome')
        options.set_capability('platformName', 'Windows 11')
        driver = webdriver.Remote(command_executor="http://192.168.1.9:4444",options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://jqueryui.com/droppable/")
        driver.implicitly_wait(10)

        # Switch to the iframe containing the drag-and-drop elements
        iframe = driver.find_element(By.CLASS_NAME, "demo-frame")
        driver.switch_to.frame(iframe)

        # Locate source and target elements
        drag_location = driver.find_element(By.XPATH, '//div[@id="draggable"]/p')
        drop_location = driver.find_element(By.XPATH, '//div[@id="droppable"]/p')

        # Get background color before drop
        color_before = drop_location.value_of_css_property("background-color")

        # Only hover over target, do not drop
        actions = ActionChains(driver)
        actions.move_to_element(drag_location)
        actions.drag_and_drop(drag_location, drag_location).perform()
        time.sleep(5)

        # Get background color after drop
        color_after = drop_location.value_of_css_property("background-color")
        driver.save_screenshot("drag_drop_negative1.png")

        # Assertion (Negative Test - should not drop in drop location)
        assert drop_location.text == "Drop here" ,"Mismatch in text displayed"
        print('Negative test passed: Drop not performed when dropped on self.')
        assert color_before == color_after, 'Drop happened'
        print('Dropped not done')

    finally:
        driver.quit()


# negative scenario with different drop location
# @pytest.mark.drag_drop_negative
def test_drag_and_drop_negative_different_drop_location():
    try:
        options = Options()
        options.add_argument('--incognito')
        options.add_argument('start-maximised')
        options.set_capability('browserName','chrome')
        options.set_capability('platformName', 'Windows 11')
        driver = webdriver.Remote(command_executor="http://192.168.1.9:4444",options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("https://jqueryui.com/droppable/")
        driver.implicitly_wait(10)

        # Switch to the iframe containing the drag-and-drop elements
        iframe = driver.find_element(By.CLASS_NAME, "demo-frame")
        driver.switch_to.frame(iframe)

        # Locate source and target elements
        drag_location = driver.find_element(By.XPATH, '//div[@id="draggable"]/p')
        drop_location = driver.find_element(By.XPATH, '//div[@id="droppable"]/p')

        # Get background color before drop
        color_before = drop_location.value_of_css_property("background-color")

        # Only hover over target, do not drop
        actions = ActionChains(driver)
        actions.click_and_hold(drag_location).move_by_offset(300, 0).pause(2).release().perform()
        time.sleep(5)

        # Get background color after drop
        color_after = drop_location.value_of_css_property("background-color")
        driver.save_screenshot("drag_drop_negative2.png")

        # Assertion (Negative Test - should not drop in drop location)
        assert drop_location.text == "Drop here" ,"Mismatch in text displayed"
        print('Negative test passed: Drop not performed when dropped on other location.')
        assert color_before == color_after, 'Drop happened'
        print('Dropped not done')

    finally:
        driver.quit()
