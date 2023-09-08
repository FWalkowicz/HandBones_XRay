namespace XRayLab.UI.DTO
{
    public class NotificationDTO
    {
        public string Message { get; set; } = default!;
        public MessageType MessageType { get; set; }

        public bool AutoHide { get; set; }

        public int DelayTimes { get; set; }
    }

    public enum MessageType
    {
        Info,
        Success,
        Error
    }
}
