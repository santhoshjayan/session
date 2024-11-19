using GeoConnect.EntityFrameworkCore;
using Volo.Abp.Autofac;
using Volo.Abp.BackgroundJobs;
using Volo.Abp.Modularity;

namespace GeoConnect.DbMigrator;

[DependsOn(
    typeof(AbpAutofacModule),
    typeof(GeoConnectEntityFrameworkCoreModule),
    typeof(GeoConnectApplicationContractsModule)
    )]
public class GeoConnectDbMigratorModule : AbpModule
{
    public override void ConfigureServices(ServiceConfigurationContext context)
    {
        Configure<AbpBackgroundJobOptions>(options => options.IsJobExecutionEnabled = false);
    }
}
