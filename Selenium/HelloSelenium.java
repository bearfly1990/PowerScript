public class App {
	private static final Logger logger = Logger.getLogger(App.class);

	public static void main(String[] args) {
		System.setProperty("webdriver.gecko.driver", "C:\\Program Files (x86)\\Mozilla Firefox\\geckodriver.exe");
		WebDriver driver = new FirefoxDriver();

		logger.info("open google!");
		driver.get("http://www.google.com");
		driver.manage().window().maximize();

		logger.info("get input id");

		WebElement textInput = driver.findElement(By.id("lst-ib"));
		WebElement submit = driver.findElement(By.name("btnK"));
		textInput.sendKeys("Selenium");
		submit.click();

		(new WebDriverWait(driver, 10)).until(new ExpectedCondition<Boolean>() {
			public Boolean apply(WebDriver driver) {
				logger.info("Title Return:" + driver.getTitle());
				return driver.getTitle().toLowerCase().startsWith("selenium");
			}
		});

		logger.info("wait 1 seconds!");
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		driver.quit();
	}
}
