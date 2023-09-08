using XRayLab.UI.DTO;

namespace XRayLab.UI.Cache
{
    public static class Error
    {
        public static List<ErrorDTO> ErrorList { get; set; }

        public static void Init()
        {
            ErrorList = new List<ErrorDTO>();
        }

        public static void AddToQueue(ErrorDTO error)
        {
            ErrorList.Add(error);
        }
    }
}
