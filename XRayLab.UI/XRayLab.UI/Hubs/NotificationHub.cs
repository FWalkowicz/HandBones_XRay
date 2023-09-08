using Microsoft.AspNetCore.SignalR;
using XRayLab.UI.DTO;

namespace XRayLab.UI.Hubs
{
    public class NotificationHub : Hub
    {
        public async Task SendNotification(NotificationDTO notificationDTO)
        {
            await Clients.All.SendAsync("notify", notificationDTO);
        }
    }
}
