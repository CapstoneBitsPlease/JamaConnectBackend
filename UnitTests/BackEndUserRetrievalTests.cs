﻿using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class BackEndUserRetrievalTests
    {
        string jamaToken;
        string jamaUsername;
        string jamaPassword;
        string jamaOrganization;
        string jamaLoginURL;
        string jamaParameters;
        HttpClient jamaLoginClient;

        string jiraToken;
        string jiraUsername;
        string jiraPassword;
        string jiraOrganization;
        string jiraLoginURL;
        string jiraParameters;
        HttpClient jiraLoginClient;

        string userURL;
        HttpClient userClient;

        [OneTimeSetUp]
        public void setup()
        {
            jamaUsername = "capstone_tester";
            jamaPassword = "capstoneBITZpls!0";
            jamaOrganization = "capstone2020";
            jamaLoginURL = "http://127.0.0.1:5000/login/jama/basic";
            jamaParameters = "?username=" + jamaUsername + "&password=" + jamaPassword + "&organization=" + jamaOrganization;
            jamaLoginClient = new HttpClient();

            jiraUsername = "bld@pdx.edu";
            jiraPassword = "kRqrISEH4OdcAz68Kg3CC018";
            jiraOrganization = "capstone2020teamb";
            jiraLoginURL = "http://127.0.0.1:5000/login/jira/basic";
            jiraParameters = "?username=" + jiraUsername + "&password=" + jiraPassword + "&organization=" + jiraOrganization;
            jiraLoginClient = new HttpClient();

            userURL = "http://127.0.0.1:5000/user";
            userClient = new HttpClient();

            jamaToken = get_jama_token();
            jiraToken = get_jira_token();

        }

        public string get_jama_token()
        {
            jamaLoginClient.BaseAddress = new Uri(jamaLoginURL + jamaParameters);
            HttpResponseMessage jama_login_response = jamaLoginClient.PostAsync(jamaLoginClient.BaseAddress, null).Result;
            if (jama_login_response.IsSuccessStatusCode)
            {
                string responseBody = jama_login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                return responseBody;
            }
            else
            {
                throw new Exception("Jama login failed! " + (int)jama_login_response.StatusCode + ": " + jama_login_response.RequestMessage);
            }
        }

        public string get_jira_token()
        {
            jiraLoginClient.BaseAddress = new Uri(jiraLoginURL + jiraParameters);
            jiraLoginClient.DefaultRequestHeaders.Add("Authorization", "Bearer " + jamaToken);
            HttpResponseMessage jira_login_response = jiraLoginClient.PostAsync(jiraLoginClient.BaseAddress, null).Result;
            if (jira_login_response.IsSuccessStatusCode)
            {
                string responseBody = jira_login_response.Content.ReadAsStringAsync().Result;
                responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                responseBody = responseBody.Substring(17);//Remove token return title.
                return responseBody;
            }
            else
            {
                throw new Exception("Jira request has failed! " + (int)jira_login_response.StatusCode + ": " + jira_login_response.RequestMessage);
            }
        }

        [Test]
        public void user_retrieval_happy_path()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer " + jiraToken);
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if (user_response.IsSuccessStatusCode)
            {
                string[] responseBody = user_response.Content.ReadAsStringAsync().Result
                                                                               .Replace("\\", "")
                                                                               .Replace("\n","")
                                                                               .Replace("\"","")
                                                                               .Replace("{","")
                                                                               .Replace("}","")
                                                                               .Trim(new char[1] { '"' })
                                                                               .Split(",");
                if(responseBody[0].Contains("true") && responseBody[1].Contains("true"))
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("One or more connections have returned false.");
                }
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
            }
        }

        /*
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
                user_client.DefaultRequestHeaders.Add("Authorization", responseBody);
                HttpResponseMessage user_response = user_client.GetAsync(userURL).Result;
                if (user_response.IsSuccessStatusCode)
                {
                    Assert.Fail("Test passed when it should not have.");
                }
                else if ((int)user_response.StatusCode == 422)
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
            else if ((int)user_response.StatusCode == 401)
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
                else if ((int)user_response.StatusCode == 401 || (int)user_response.StatusCode == 422)
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
        */
    }
}
