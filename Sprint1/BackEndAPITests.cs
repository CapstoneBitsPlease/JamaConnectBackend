using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.Sprint1
{
    class BackEndAPITests
    {
        string username;
        string password;
        string organization;
        string url;
        HttpClient client;
        string correct_parameters;
        string test_parameters;
        [OneTimeSetUp]
        public void setup()
        {
            username = "bld";
            password = "September217";
            organization = "capstone2020";
            url = "http://127.0.0.1:5000/login/basic";
            client = new HttpClient();
            //?username=bld&password=September217&organization=capstone2020
            correct_parameters = "?username=" + username + "&password=" + password + "&organization=" + organization;
            client.BaseAddress = new Uri(url+correct_parameters);
        }

        [Test]
        public void login_happy_path_test()
        {
            HttpResponseMessage response = client.PostAsync(client.BaseAddress,null).Result; 
            if(response.IsSuccessStatusCode)
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
