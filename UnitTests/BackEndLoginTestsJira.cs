using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class BackEndLoginTestsJira
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
                url = "http://127.0.0.1:5000/login/jira/basic";
                client = new HttpClient();
                //?username=bld&password=September217&organization=capstone2020
                correct_parameters = "?username=" + username + "&password=" + password + "&organization=" + organization;
            }

            [Test]
            public void login_happy_path_test()
            {
                client.BaseAddress = new Uri(url + correct_parameters);
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
            public void login_bad_password()
            {
                test_parameters = "?username=" + username + "&password=badpassword&organization=" + organization;
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
                test_parameters = "?username=" + username + "&password=" + password + "&organization=badorganzation";
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
            public void login_bad_username_and_bade_password()
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
                test_parameters = "?username=basusername&password=" + password + "&organization=badorganization";
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
            public void login_bad_password_and_bad_organization()
            {
                test_parameters = "?username=" + username + "&password=badpassword&organization=badorganization";
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
                else if ((int)response.StatusCode == 401)
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
}
