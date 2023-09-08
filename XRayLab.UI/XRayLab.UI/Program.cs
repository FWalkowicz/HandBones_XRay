using XRayLab.UI.Hubs;

namespace XRayLab.UI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            Cache.Success.Init();
            Cache.Error.Init();

            //================================
            var builder = WebApplication.CreateBuilder(args);


            builder.Services.AddSignalR();
            builder.Services.AddSingleton<NotificationHub>();

            builder.Services.AddHostedService<BackendNotificationService>();
            builder.Services.AddScoped<BackendNotificationService>();


            // Add services to the container.
            builder.Services.AddControllersWithViews();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (!app.Environment.IsDevelopment())
            {
                app.UseExceptionHandler("/Home/Error");
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseStaticFiles();

            app.UseRouting();

            app.UseAuthorization();

            app.MapControllerRoute(
                name: "default",
                pattern: "{controller=Home}/{action=Index}/{id?}");

            app.Run();
        }
    }
}