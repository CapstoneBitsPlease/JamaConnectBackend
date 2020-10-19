using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.Sprint1
{
    class BackEndUserRetrievalTests
    {
        string token;
        string username;
        string password;
        string organization;
        string loginURL;
        string userURL;
        HttpClient client;
        string correct_parameters;

        [OneTimeSetUp]
        public void setup()
        {
            username = "bld";
            password = "September217";
            organization = "capstone2020";
            loginURL = "http://127.0.0.1:5000/login/basic";
            userURL = "http://127.0.0.1:5000/user";
            client = new HttpClient();
            correct_parameters = "?username=" + username + "&password=" + password + "&organization=" + organization;
        }

        [Test]
        public void user_retrival_happy_path()
        {
            client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Request has failed!");
            }
        }
    }
}
