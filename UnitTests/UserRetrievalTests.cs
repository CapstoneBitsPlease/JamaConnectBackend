using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using NUnit.Framework;
using OpenQA.Selenium;

namespace PSUCapstoneTestingProject.Back_end.UnitTests
{
    class UserRetrievalTests
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
                                                                               .Replace("\n", "")
                                                                               .Replace("\"", "")
                                                                               .Replace("{", "")
                                                                               .Replace("}", "")
                                                                               .Trim(new char[1] { '"' })
                                                                               .Split(",");
                if (responseBody[0].Contains("true") && responseBody[1].Contains("true"))
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

        [Test]
        public void user_retrieval_with_jama_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer " + jamaToken);
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if (user_response.IsSuccessStatusCode)
            {
                string[] responseBody = user_response.Content.ReadAsStringAsync().Result
                                                                               .Replace("\\", "")
                                                                               .Replace("\n", "")
                                                                               .Replace("\"", "")
                                                                               .Replace("{", "")
                                                                               .Replace("}", "")
                                                                               .Trim(new char[1] { '"' })
                                                                               .Split(",");
                if (responseBody[0].Contains("true"))
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Jama token returned false.");
                }

                if(responseBody[1].Contains("false"))
                {
                    Assert.Pass();
                }
                else
                {
                    Assert.Fail("Jira token returned true.");
                }
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);
            }
        }

        [Test]
        public void user_retrieval_without_auth_header()
        {
            userClient.BaseAddress = new Uri(userURL);
            //userClient.DefaultRequestHeaders.Add("Authorization", "Bearer " + jamaToken);
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 400 || (int)user_response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else
            {
                Assert.Fail("Login request passed when it should not have.");
            }
        }

        [Test]
        public void user_retrieval_without_bearer_keyword_jama_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", jamaToken);
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 400 || (int)user_response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else if(user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }

        [Test]
        public void user_retrieval_without_bearer_keyword_jira_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", jiraToken);
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 400 || (int)user_response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else if (user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }

        [Test]
        public void user_retrieval_expired_jira_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDM1NjEzMjIsIm5iZiI6MTYwMzU2MTMyMiwianRpIjoiNTQ4YjUyYWQtMWE3YS00YTY0LTg3OTMtNGRjY2FlOWIxM2JhIiwiZXhwIjoxNjAzNTYyMjIyLCJpZGVudGl0eSI6eyJjb25uZWN0aW9uX2lkIjoiYjc4Y2I4MzEtYTQ3ZC00ZWU1LTkyNDAtYTgyMThkYjM2MWRiIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.b0psrxqkie6XOkqwEG0L8zJh1lL6bp17O_SA4Bi45Ss");
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else if (user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }

        [Test]
        public void user_retrieval_expired_jama_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDM1NzAxNDQsIm5iZiI6MTYwMzU3MDE0NCwianRpIjoiMWZlNGNkYTgtNTQ1My00MzljLWI2MTAtODExN2IzNTgzNzNlIiwiZXhwIjoxNjAzNTcxMDQ0LCJpZGVudGl0eSI6eyJjb25uZWN0aW9uX2lkIjoiOGE3YWE1Y2UtNzk2OS00NzFmLThmZDMtNjYxOTBkYTYwZTE5In0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.VFe7WSpdy5oKF4e0UDE73ecVCdNwFEET5Ij949A_UOQ");
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else if (user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }

        [Test]
        public void user_retrieval_bad_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer badtokenhere");
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 401)
            {
                Assert.Pass();
            }
            else if (user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }

        [Test]
        public void user_retrieval_empty_token()
        {
            userClient.BaseAddress = new Uri(userURL);
            userClient.DefaultRequestHeaders.Add("Authorization", "Bearer");
            HttpResponseMessage user_response = userClient.GetAsync(userURL).Result;
            if ((int)user_response.StatusCode == 422)
            {
                Assert.Pass();
            }
            else if (user_response.IsSuccessStatusCode)
            {
                Assert.Fail("Login request passed when it should not have.");
            }
            else
            {
                Assert.Fail("The user request did not succeed. " + (int)user_response.StatusCode + ": " + user_response.RequestMessage);

            }
        }
    }
}