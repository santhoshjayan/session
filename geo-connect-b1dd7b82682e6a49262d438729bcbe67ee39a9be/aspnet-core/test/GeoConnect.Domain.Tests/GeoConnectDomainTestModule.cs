using GeoConnect.EntityFrameworkCore;
using Volo.Abp.Modularity;

namespace GeoConnect;

[DependsOn(
    typeof(GeoConnectEntityFrameworkCoreTestModule)
    )]
public class GeoConnectDomainTestModule : AbpModule
{

}
