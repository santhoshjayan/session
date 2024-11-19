using System.Threading.Tasks;

namespace GeoConnect.Data;

public interface IGeoConnectDbSchemaMigrator
{
    Task MigrateAsync();
}
