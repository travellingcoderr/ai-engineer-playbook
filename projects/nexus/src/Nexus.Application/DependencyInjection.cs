using Microsoft.Extensions.DependencyInjection;
using Nexus.Application.Services;

namespace Nexus.Application
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddApplicationServices(this IServiceCollection services)
        {
            services.AddScoped<ITransferService, TransferService>();
            return services;
        }
    }
}
