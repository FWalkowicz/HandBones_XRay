namespace XRayLab.UI.Core
{
    public static class ULRs
    {
#if DEBUG
        public static string XRayAPIURL = "http://192.168.2.116:8003";
#else
        public static string XRayAPIURL = Environment.GetEnvironmentVariable("APIURL");
#endif
    }
}
