namespace XRayLab.UI.DTO
{
    public class SessionListDTO
    {
        public string UniqueSessionId { get; set; }
        public FileDTO[] Files { get; set; }
    }

    public class FileDTO
    {
        public string FileName { get; set; }
        public string Type { get; set; }
        public string FriendlyName
        {
            get
            {
                return Path.GetFileNameWithoutExtension(FileName);
            }
        }
    }
}
