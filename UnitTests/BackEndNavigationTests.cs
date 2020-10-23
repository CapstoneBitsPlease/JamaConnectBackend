using System;
using System.Collections;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;


namespace PSUCapstoneTestingProject.Back_end
{
    public class ChromeBackEndAPITests
    {
        IWebDriver driver;
        string index_url;
        [OneTimeSetUp]
        public void Setup()
        {
            driver = new ChromeDriver("C:/Users/Brandon Danielski/Documents");
            index_url = "http://127.0.0.1:5000/index";
            
        }
        [Test]
        public void index_ping()
        {
            driver.Url = index_url;
            driver.Navigate();
            Assert.IsTrue(driver.FindElement(By.TagName("Body")).Text.Equals("hello world"));
        }
    }
}