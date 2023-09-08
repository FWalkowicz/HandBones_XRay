using XRayLab.UI.DTO;

namespace XRayLab.UI.Cache
{
    public static class Success
    {
        public static List<SuccessDTO> SuccessList { get; set; }

        public static void Init()
        {
            SuccessList = new List<SuccessDTO>();
        }

        public static void AddToQueue(SuccessDTO error)
        {
            SuccessList.Add(error);
        }
    }
}
