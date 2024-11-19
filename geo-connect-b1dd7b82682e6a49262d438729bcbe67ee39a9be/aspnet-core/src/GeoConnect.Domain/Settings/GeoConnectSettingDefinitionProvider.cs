using Volo.Abp.Settings;

namespace GeoConnect.Settings;

public class GeoConnectSettingDefinitionProvider : SettingDefinitionProvider
{
    public override void Define(ISettingDefinitionContext context)
    {
        //Define your own settings here. Example:
        //context.Add(new SettingDefinition(GeoConnectSettings.MySetting1));
    }
}
