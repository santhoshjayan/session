using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;

namespace GeoConnect.Data;

/* This is used if database provider does't define
 * IGeoConnectDbSchemaMigrator implementation.
 */
public class NullGeoConnectDbSchemaMigrator : IGeoConnectDbSchemaMigrator, ITransientDependency
{
    public Task MigrateAsync()
    {
        return Task.CompletedTask;
    }
}
