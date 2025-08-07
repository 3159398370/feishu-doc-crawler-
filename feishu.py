from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def create_driver():
    """创建浏览器驱动实例"""
    # 设置 ChromeDriver 路径
    driver_path = "chromedriver.exe"
    service = Service(executable_path=driver_path)

    # 设置浏览器选项 - 启用无头模式
    options = Options()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=service, options=options)

def crawl_feishu_document(url, filename):
    """爬取飞书文档并保存到指定文件"""
    browser = None
    try:
        # 启动浏览器
        browser = create_driver()

        # 访问用户提供的URL
        browser.get(url)

        # 等待页面内容加载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 获取页面文本内容
        full_text = browser.find_element(By.TAG_NAME, "body").text

        # 保存到文件
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"文档内容已成功保存到 {filename}")
        return True

    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
        return False

    finally:
        # 确保浏览器被正确关闭
        if browser:
            browser.quit()

def get_next_filename(folder_path, base_name="feishu"):
    """获取下一个可用的文件名"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    index = 1
    while True:
        filename = os.path.join(folder_path, f"{base_name}_{index}.txt")
        if not os.path.exists(filename):
            return filename
        index += 1

def main():
    """主函数"""
    # 创建保存文件的文件夹
    folder_path = "feishu_documents"

    print("飞书文档爬虫程序")
    print("输入 'quit' 或 'exit' 退出程序")

    while True:
        # 获取用户输入
        user_input = input("\n请输入需要爬虫的文档URL: ").strip()

        # 检查退出条件
        if user_input.lower() in ['quit', 'exit']:
            print("程序已退出")
            break

        if not user_input:
            print("URL不能为空，请重新输入")
            continue

        # 获取下一个可用的文件名
        filename = get_next_filename(folder_path)

        # 爬取文档
        success = crawl_feishu_document(user_input, filename)

        if success:
            print(f"第 {filename.split('_')[-1].split('.')[0]} 个文档爬取完成")

if __name__ == "__main__":
    main()
