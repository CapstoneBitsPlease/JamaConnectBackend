﻿using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class BackEndLoginTestsJama
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
            username = "capstone_tester";
            password = "capstoneBITZpls!0";
            organization = "capstone2020";
            url = "http://127.0.0.1:5000/login/jama/basic";
            client = new HttpClient();
            //?username=bld&password=September217&organization=capstone2020
            correct_parameters = "?username=" + username + "&password=" + password + "&organization=" + organization;
        }

        [Test]
        public void login_happy_path_test()
        {
            client.BaseAddress = new Uri(url + correct_parameters);
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

        [Test]
        public void login_bad_username()
        {
            test_parameters = "?username=BadUsername&password=" + password + "&organization=" + organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if((int)response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: "+ (int)response.StatusCode+": "+response.RequestMessage);
            }

        }

        [Test]
        public void login_bad_password()
        {
            test_parameters = "?username="+username+"&password=badpassword&organization=" + organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }

        [Test]
        public void login_bad_organization()
        {
            test_parameters = "?username=" + username + "&password="+password+"&organization=badorganzation";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }
        [Test]
        public void login_bad_username_and_bad_password()
        {
            test_parameters = "?username=basusername&password=badpassword&organization=" + organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }
        [Test]
        public void login_bad_username_and_bad_organization()
        {
            test_parameters = "?username=basusername&password="+password+"&organization=badorganization";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }

        [Test]
        public void login_bad_password_and_bad_organization()
        {
            test_parameters = "?username="+username+"&password=badpassword&organization=badorganization";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }
        [Test]
        public void login_bad_username_bad_password_and_bad_organization()
        {
            test_parameters = "?username=badusername&password=badpassword&organization=badorganization";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }

        }
        [Test]
        public void login_no_username()
        {
            test_parameters = "?username=&password="+password+"&organization="+organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_password()
        {
            test_parameters = "?username="+username+"&password=&organization=" + organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_organization()
        {
            test_parameters = "?username=" + username + "&password="+password+"&organization=";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_username_or_password()
        {
            test_parameters = "?username=&password=&organization="+organization;
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_username_or_organization()
        {
            test_parameters = "?username=&password="+password+"&organization=";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_password_or_ogranization()
        {
            test_parameters = "?username="+username+"&password=&organization=";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_password_username_or_organization()
        {
            test_parameters = "?username=&password=&organization=";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 401 || (int)response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
        [Test]
        public void login_no_query()
        {
            test_parameters = "";
            client.BaseAddress = new Uri(url + test_parameters);
            HttpResponseMessage response = client.PostAsync(client.BaseAddress, null).Result;
            if (response.IsSuccessStatusCode)
            {
                Assert.Fail("Request passed when it should not have.");
            }
            else if ((int)response.StatusCode == 400)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Incorrect request code: " + (int)response.StatusCode + ": " + response.RequestMessage);
            }
        }
    }
}
