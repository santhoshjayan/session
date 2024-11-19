using Volo.Abp.DependencyInjection;
using Volo.Abp.Ui.Branding;

namespace GeoConnect;

[Dependency(ReplaceServices = true)]
public class GeoConnectBrandingProvider : DefaultBrandingProvider
{
    public override string AppName => "GeoConnect";
}
