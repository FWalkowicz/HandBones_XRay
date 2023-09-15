using Newtonsoft.Json;
using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using XRayLab.UI.Core;
using XRayLab.UI.DTO;

namespace XRayLab.UI.ApiWrapper
{
    public class XRayAPI
    {
        private string WebApiUrl = ULRs.XRayAPIURL;
        private HttpClient client;

        public XRayAPI()
        {
            var httpHandler = new HttpClientHandler
            {
                ServerCertificateCustomValidationCallback = (o, cert, chain, errors) => true
            };


            client = new HttpClient(httpHandler);
            client.BaseAddress = new Uri(WebApiUrl);
            client.DefaultRequestHeaders.Clear();
            client.DefaultRequestHeaders.ConnectionClose = true;

            var clientId = "comcore";
            var clientSecret = "75TF3R7HrqFB";
            var authenticationString = $"{clientId}:{clientSecret}";
            var base64EncodedAuthenticationString = Convert.ToBase64String(System.Text.ASCIIEncoding.UTF8.GetBytes(authenticationString));

            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", base64EncodedAuthenticationString);
        }

        public SessionListDTO POST_ExecuteAI(byte[] byteArray, string fileName)
        {
            try
            {
                //HttpContent content = new StreamContent(body);
                //content.Headers.ContentType = new MediaTypeHeaderValue("multipart/form-data");

                //var response = client.PostAsync($"executeAI", new StreamContent(body)).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                //SessionListDTO sessionList = JsonConvert.DeserializeObject<SessionListDTO>(content);

                MultipartFormDataContent form = new MultipartFormDataContent();

                form.Add(new ByteArrayContent(byteArray, 0, byteArray.Length), "input_image", $"{fileName}");
                HttpResponseMessage response = client.PostAsync("executeAI", form).Result;

                response.EnsureSuccessStatusCode();
                string result = response.Content.ReadAsStringAsync().Result;

                SessionListDTO sessionList = JsonConvert.DeserializeObject<SessionListDTO>(result);

                return sessionList;

            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "ExecuteAI"
                });
                return null;
            }
        }

        public SessionListDTO GET_Sessions()
        {
            try
            {
                var result = client.GetAsync($"sessions").Result;
                var content = result.Content.ReadAsStringAsync().Result;
                
                SessionListDTO sessionList = JsonConvert.DeserializeObject<SessionListDTO>(content);
                return sessionList;

            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "GetMeasure"
                });
                return null;
            }
        }

        public List<FileDTO> GET_Session(string uniqueSessionId)
        {
            try
            {
                var result = client.GetAsync($"session/{{uniqueSessionId}}?unique_session_id={uniqueSessionId}").Result;
                var content = result.Content.ReadAsStringAsync().Result;

                List<FileDTO> sessionList = JsonConvert.DeserializeObject<List<FileDTO>>(content);
                return sessionList;

            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "GetMeasure"
                });
                return null;
            }
        }

        public Stream GET_UniqueSessionImage(string uniqueSessionId, string fileName)
        {
            try
            {
                var result = client.GetStreamAsync($"session/{uniqueSessionId}/image/{fileName}").Result;
                return result;

            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "GetMeasure"
                });
                return null;
            }
        }

        public string GET_UniqueSessionMeta(string uniqueSessionId, string metadata)
        {
            try
            {
                var result = client.GetAsync($"session/{uniqueSessionId}/meta/{metadata}").Result;
                var content = result.Content.ReadAsStringAsync().Result;

                return content;

            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "GetMeasure"
                });
                return null;
            }
        }

        public void DELETE_UniqueSession(string uniqueSessionId)
        {
            try
            {
                var result = client.DeleteAsync($"session/{uniqueSessionId}").Result;
                var content = result.Content.ReadAsStringAsync().Result;
            }
            catch (Exception er)
            {
                Cache.Error.AddToQueue(new ErrorDTO()
                {
                    Message = er.Message,
                    Class = nameof(XRayAPI),
                    Method = "GetMeasure"
                });
            }
        }

    }
}
