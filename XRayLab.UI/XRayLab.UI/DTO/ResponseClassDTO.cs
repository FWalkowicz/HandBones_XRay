namespace XRayLab.UI.DTO
{
    public class ResponseClassDTO
    {
        public string UniqueSessionId { get; set; }
        public string ImageBase64 { get; set; }
        public string Description { get;  set; }
        public List<FileDTO> Files { get;  set; }
    }
}
