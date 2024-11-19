using Volo.Abp.Modularity;

namespace GeoConnect;

[DependsOn(
    typeof(GeoConnectApplicationModule),
    typeof(GeoConnectDomainTestModule)
    )]
public class GeoConnectApplicationTestModule : AbpModule
{

}
