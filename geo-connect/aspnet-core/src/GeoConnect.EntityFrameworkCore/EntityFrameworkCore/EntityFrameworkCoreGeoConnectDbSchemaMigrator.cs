using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using GeoConnect.Data;
using Volo.Abp.DependencyInjection;

namespace GeoConnect.EntityFrameworkCore;

public class EntityFrameworkCoreGeoConnectDbSchemaMigrator
    : IGeoConnectDbSchemaMigrator, ITransientDependency
{
    private readonly IServiceProvider _serviceProvider;

    public EntityFrameworkCoreGeoConnectDbSchemaMigrator(
        IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task MigrateAsync()
    {
        /* We intentionally resolving the GeoConnectDbContext
         * from IServiceProvider (instead of directly injecting it)
         * to properly get the connection string of the current tenant in the
         * current scope.
         */

        await _serviceProvider
            .GetRequiredService<GeoConnectDbContext>()
            .Database
            .MigrateAsync();
    }
}
