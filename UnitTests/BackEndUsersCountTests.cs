using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class BackEndUsersCountTests
    {
        string token;
        string username;
        string password;
        string organization;
        string loginURL;
        string userURL;
        HttpClient login_client;
        HttpClient user_client;
        string correct_parameters;

        [OneTimeSetUp]
        public void setup()
        {
            username = "capstone_tester";
            password = "capstoneBITZpls!0";
            organization = "capstone2020";
            loginURL = "http://127.0.0.1:5000/login/jama/basic";
            userURL = "http://127.0.0.1:5000/user";
            login_client = new HttpClient();
            user_client = new HttpClient();
            correct_parameters = "?username=" + username + "&password=" + password + "&organization=" + organization;
        }

        [Test]
        public void user_retrieval_happy_path()
        {
            login_client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage login_response = login_client.PostAsync(login_client.BaseAddress, null).Result;
           
            if (login_response.IsSuccessStatusCode)
            {
                string responseBody = login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length-3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                user_client.BaseAddress = new Uri(userURL);
                user_client.DefaultRequestHeaders.Add("Authorization","Bearer "+responseBody);
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if(user_response.IsSuccessStatusCode)
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("The user request did not succeed.");
                }
            }
            else
            {
                Assert.Fail("Login has failed!");
            }
        }

        [Test]
        public void user_retrieval_without_bearer_keyword()
        {
            login_client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage login_response = login_client.PostAsync(login_client.BaseAddress, null).Result;

            if (login_response.IsSuccessStatusCode)
            {
                string responseBody = login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                user_client.BaseAddress = new Uri(userURL);
                user_client.DefaultRequestHeaders.Add("Authorization",responseBody);
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("Test passed when it should not have.");
                }
                else if((int)user_response.StatusCode == 422)
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Incorrect request code: " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
                }
            }
            else
            {
                Assert.Fail("Login has failed!");
            }
        }

        [Test]
        public void user_retrieval_with_expired_token()
        {
                user_client.BaseAddress = new Uri(userURL);
                user_client.DefaultRequestHeaders.Add("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDMyMjcyNDAsIm5iZiI6MTYwMzIyNzI0MCwianRpIjoiNDU2M2E5M2EtMDU3MC00ZTljLWJjMjgtOWU3ZGIzNGZkNDQ5IiwiZXhwIjoxNjAzMjI4MTQwLCJpZGVudGl0eSI6eyJ1c2VybmFtZSI6ImJsZCIsImNvbm5lY3Rpb25faWQiOiI3NmZhYWQ5NC02YWY5LTRiMmItYjg0OS1iM2M0OTBiMTE3MDAifSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.QdCbC6CRfpDD3oXXcVp4Ul24XO-AwhGtntSaIbz8Az4");
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("The user request passed when it should not have.");
                }
                else if((int)user_response.StatusCode == 401)
                {
                    Assert.Pass();
                }
                else
                {
                   Assert.Fail("Incorrect request code: " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
                }
        }

        [Test]
        public void user_retrieval_with_bad_token()
        {
            login_client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage login_response = login_client.PostAsync(login_client.BaseAddress, null).Result;

            if (login_response.IsSuccessStatusCode)
            {
                string responseBody = login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                user_client.BaseAddress = new Uri(userURL);
                user_client.DefaultRequestHeaders.Add("Authorization", "Bearer badtokensbewe12321");
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("Request passed when it should not have.");
                }
                else if((int)user_response.StatusCode == 401 || (int)user_response.StatusCode == 422)
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Incorrect request code: " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
                }
            }
            else
            {
                Assert.Fail("Login has failed!");
            }
        }

        [Test]
        public void user_retrieval_with_no_header()
        {
            login_client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage login_response = login_client.PostAsync(login_client.BaseAddress, null).Result;

            if (login_response.IsSuccessStatusCode)
            {
                string responseBody = login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                user_client.BaseAddress = new Uri(userURL);
                //user_client.DefaultRequestHeaders.Add("Authorization", "Bearer badtokensbewe12321");
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("Request passed when it should not have.");
                }
                else if ((int)user_response.StatusCode == 401)
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Incorrect request code: " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
                }
            }
            else
            {
                Assert.Fail("Login has failed!");
            }
        }

        [Test]
        public void user_retrieval_with_bad_header_title()
        {
            login_client.BaseAddress = new Uri(loginURL + correct_parameters);
            HttpResponseMessage login_response = login_client.PostAsync(login_client.BaseAddress, null).Result;

            if (login_response.IsSuccessStatusCode)
            {
                string responseBody = login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                user_client.BaseAddress = new Uri(userURL);
                user_client.DefaultRequestHeaders.Add("BadTitle", "Bearer " + responseBody);
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("Request passed when it should not have.");
                }
                else if ((int)user_response.StatusCode == 401)
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Incorrect request code: " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
                }
            }
            else
            {
                Assert.Fail("Login has failed!");
            }
        }
    }
}
