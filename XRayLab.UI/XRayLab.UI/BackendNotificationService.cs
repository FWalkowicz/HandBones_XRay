using Microsoft.AspNetCore.SignalR;
using XRayLab.UI.DTO;
using XRayLab.UI.Hubs;

namespace XRayLab.UI
{
    public class BackendNotificationService : BackgroundService
    {
        private readonly ILogger<BackendNotificationService> _logger;
        private readonly IHubContext<NotificationHub> _notificationHub;
        private bool _notificationSent = false;

        public BackendNotificationService(ILogger<BackendNotificationService> logger, IHubContext<NotificationHub> notificationHub)
        {
            _logger = logger;
            _notificationHub = notificationHub;
        }

        protected async override Task ExecuteAsync(CancellationToken stoppingToken)
        {

            while (!stoppingToken.IsCancellationRequested)
            {
                if (!_notificationSent)
                {
                    var successItem = Cache.Success.SuccessList.FirstOrDefault();
                    var errorItem = Cache.Error.ErrorList.FirstOrDefault();

                    //===Error====
                    if (errorItem != null)
                    {
                        var _errorItem = new NotificationDTO()
                        {
                            AutoHide = true,
                            Message = $"{errorItem.Class}: {errorItem.Message}",
                            DelayTimes = 4000,
                            MessageType = MessageType.Error
                        };

                        await TriggerNotification(_errorItem);
                        if (Cache.Error.ErrorList.Count > 0)
                            Cache.Error.ErrorList.RemoveAt(0);
                    }

                    if (successItem != null)
                    {
                        var _successItem = new NotificationDTO()
                        {
                            AutoHide = true,
                            Message = successItem.Message,
                            DelayTimes = 4000,
                            MessageType = MessageType.Success
                        };

                        await TriggerNotification(_successItem);
                        if (Cache.Success.SuccessList.Count > 0)
                            Cache.Success.SuccessList.RemoveAt(0);
                    }
                }
                await Task.Delay(2000);
            }
        }


        public Task TriggerNotification(NotificationDTO notification)
        {
            _notificationHub.Clients.All.SendAsync("notify", notification);
            return Task.CompletedTask;

        }
    }
}
