using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class BackEndMultiUserRetrievalTests
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
        HttpClient user_client;
        string correct_parameters;

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
  
        }
    }
}
