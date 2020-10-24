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
            string jama_username;
            string jama_password;
            string jama_organization;
            string jama_url;
            HttpClient jama_client;
            string correct_jama_parameters;

            string jira_username;
            string jira_password;
            string jira_organization;
            string jira_url;
            HttpClient jira_client;
            string correct_jira_parameters;

            string test_parameters;
            string jama_token;

            [OneTimeSetUp]
            public void setup()
            {


                jira_username = "bld@pdx.edu";
                jira_password = "kRqrISEH4OdcAz68Kg3CC018";
                jira_organization = "capstone2020teamb";
                jira_url = "http://127.0.0.1:5000/login/jira/basic";
                jira_client = new HttpClient();
                correct_jira_parameters = "?username=" + jira_username + "&password=" + jira_password + "&organization=" + jira_organization;

                jama_username = "capstone_tester";
                jama_password = "capstoneBITZpls!0";
                jama_organization = "capstone2020";
                jama_url = "http://127.0.0.1:5000/login/jama/basic";
                jama_client = new HttpClient();
                correct_jama_parameters = "?username=" + jama_username + "&password=" + jama_password + "&organization=" + jama_organization;

                jama_token = get_jama_token();
                
            }

            public string get_jama_token()
            {
                jama_client.BaseAddress = new Uri(jama_url + correct_jama_parameters);
                HttpResponseMessage jama_login_response = jama_client.PostAsync(jama_client.BaseAddress, null).Result;
                if(jama_login_response.IsSuccessStatusCode)
                {
                    string responseBody = jama_login_response.Content.ReadAsStringAsync().Result;
                    responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                    responseBody = responseBody.Substring(17);//Remove token return title.
                    return responseBody;
                }
                else
                {
                    throw new Exception("Jama login failed! "+ (int)jama_login_response.StatusCode + ": " + jama_login_response.RequestMessage);
                }
            }

            [Test]
            public void login_happy_path_test()
            {
                    jira_client.BaseAddress = new Uri(jira_url + correct_jira_parameters);
                    jira_client.DefaultRequestHeaders.Add("Authorization", "Bearer " + jama_token);
                    HttpResponseMessage jira_login_response = jira_client.PostAsync(jira_client.BaseAddress,null).Result;
                    if(jira_login_response.IsSuccessStatusCode)
                    {
                        Assert.Pass();
                    }
                    else
                    {
                        Assert.Fail("Jira request has failed! "+ (int)jira_login_response.StatusCode + ": " + jira_login_response.RequestMessage);
                    }
            }

            [Test]
            public void login_bad_username()
            {
                test_parameters = "?username=BadUsername&password=" + jira_password + "&organization=" + jira_organization;
                jira_client.BaseAddress = new Uri(jira_url + test_parameters);
                jira_client.DefaultRequestHeaders.Add("Authorization", "Bearer " + jama_token);
                HttpResponseMessage response = jira_client.PostAsync(jira_client.BaseAddress, null).Result;
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
                test_parameters = "?username="+jira_username+"&password=badpassword&organization=" + jira_organization;
                jira_client.BaseAddress = new Uri(jira_url + test_parameters);
                jira_client.DefaultRequestHeaders.Add("Authorization", "Bearer " + jama_token);
                HttpResponseMessage response = jira_client.PostAsync(jira_client.BaseAddress, null).Result;
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
                test_parameters = "?username=" + jira_username + "&password="+jira_password+"&organization=badorganization";
                jira_client.BaseAddress = new Uri(jira_url + test_parameters);
                jira_client.DefaultRequestHeaders.Add("Authorization", "Bearer " + jama_token);
                HttpResponseMessage response = jira_client.PostAsync(jira_client.BaseAddress, null).Result;
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
