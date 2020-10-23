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

            [OneTimeSetUp]
            public void setup()
            {


                jira_username = "bld@pdx.edu";
                jira_password = "kRqrISEH4OdcAz68Kg3CC018";
                jira_organization = "capstone2020teamb";
                jira_url = "http://127.0.0.1:5000/login/jira/basic";
                jira_client = new HttpClient();
                //correct_jira_parameters = "?username=" + jira_username + "&password=" + password + "&organization=" + jira_organization;

                jama_username = "capstone_tester";
                jama_password = "capstoneBITZpls!0";
                jama_organization = "capstone2020";
                jama_url = "http://127.0.0.1:5000/login/jama/basic";
                jama_client = new HttpClient();
                correct_jama_parameters = "?username=" + jama_username + "&password=" + jama_password + "&organization=" + jama_organization;
            }

            [Test]
            public void login_happy_path_test()
            {
                jama_client.BaseAddress = new Uri(jama_url + correct_jama_parameters);
                HttpResponseMessage jama_login_response = jama_client.PostAsync(jama_client.BaseAddress, null).Result;
                if (jama_login_response.IsSuccessStatusCode)
                {
                    string responseBody = jama_login_response.Content.ReadAsStringAsync().Result;
                    responseBody = responseBody.Remove(responseBody.Length - 3);//Remove the ' "} ' from end of token.
                    responseBody = responseBody.Substring(17);//Remove token return title.
                    correct_jira_parameters = "?username=" + jira_username + "&password=" + responseBody + "&organization=" + jira_organization;
                    jira_client.BaseAddress = new Uri(jira_url + correct_jira_parameters);
                    jira_client.DefaultRequestHeaders.Add("Authorization", "Bearer " + responseBody);
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
                else
                {
                    Assert.Fail("Jama request has failed!"+ (int)jama_login_response.StatusCode + ": " + jama_login_response.RequestMessage);
                }
            }
        }
    }
}
