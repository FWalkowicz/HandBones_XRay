using System.Text;
using XRayLab.UI.Core;
using XRayLab.UI.DTO;

namespace XRayLab.UI.ApiWrapper
{
    public static class XRayAPI
    {
        private static string WebApiUrl = ULRs.XRayAPIURL;
        private static HttpClient client;

        public static void Init()
        {
            var httpHandler = new HttpClientHandler
            {
                ServerCertificateCustomValidationCallback = (o, cert, chain, errors) => true
            };


            client = new HttpClient(httpHandler);
            client.BaseAddress = new Uri(WebApiUrl);
        }

        public static string POST_ExecuteAI(MeasureRequest body)
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        public static string GET_Sessions()
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        public static string GET_Session(string uniqueSessionId)
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        public static string GET_UniqueSessionImage(string uniqueSessionId,string filename)
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        public static string GET_UniqueSessionMeta(string uniqueSessionId, string metadata)
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        public static string DELETE_UniqueSession(string uniqueSessionId, string metadata)
        {
            try
            {
                //var serializedItem = JsonConvert.SerializeObject(body);
                //var response = client.PostAsync($"GetMeasure", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
                //var content = response.Content.ReadAsStringAsync().Result;
                return null;

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

        //public static MeasureResponse GetMeasureFaster(MeasureRequest body)
        //{
        //    try
        //    {
        //        var serializedItem = JsonConvert.SerializeObject(body);
        //        var response = client.PostAsync($"GetMeasureFaster", new StringContent(serializedItem, Encoding.UTF8, "application/json")).Result;
        //        var content = response.Content.ReadAsStringAsync().Result;
        //        return JsonConvert.DeserializeObject<MeasureResponse>(content);

        //    }
        //    catch (Exception er)
        //    {
        //        Cache.Error.AddToQueue(new ErrorDTO()
        //        {
        //            Message = er.Message,
        //            Class = nameof(BroadSens),
        //            Method = "GetMeasureFaster"
        //        });
        //        return null;
        //    }
        //}

        //public static void InitSensors()
        //{
        //    try
        //    {
        //        var result = client.GetAsync($"InitSensors").Result;
        //        var content = result.Content.ReadAsStringAsync().Result;
        //        Cache.Cache.BroadSenseSetting = JsonConvert.DeserializeObject<InitBroadSenseResponse>(content);


        //        for (int i = 0; i < 4; i++)
        //        {
        //            var deviceData = Cache.Cache.BroadSenseSetting?.DeviceDatas[0];

        //            Cache.Cache.StausMeasurement[i].Gain = deviceData.Channels[i].GainInit.HasValue ? deviceData.Channels[i].GainInit.Value : 0;
        //            Cache.Cache.StausMeasurement[i].ColorClass = BootStrapColorEnum.@default.ToString();
        //        }
        //    }
        //    catch (Exception er)
        //    {
        //        Cache.Error.AddToQueue(new ErrorDTO()
        //        {
        //            Message = er.Message,
        //            Class = nameof(BroadSens),
        //            Method = "InitSensors"
        //        });
        //    }
        //}

        //public static void SetProbes()
        //{
        //    try
        //    {
        //        var result = client.GetAsync($"SetProbesPerSek/{Cache.Settings.ProbesPerSec}").Result;
        //    }
        //    catch (Exception er)
        //    {
        //        Cache.Error.AddToQueue(new ErrorDTO()
        //        {
        //            Message = er.Message,
        //            Class = nameof(BroadSens),
        //            Method = "SetProbes"
        //        });
        //    }
        //}
    }
}
