using GeoConnect.Localization;
using Volo.Abp.Authorization.Permissions;
using Volo.Abp.Localization;

namespace GeoConnect.Permissions;

public class GeoConnectPermissionDefinitionProvider : PermissionDefinitionProvider
{
    public override void Define(IPermissionDefinitionContext context)
    {
        var myGroup = context.AddGroup(GeoConnectPermissions.GroupName);
        //Define your own permissions here. Example:
        //myGroup.AddPermission(GeoConnectPermissions.MyPermission1, L("Permission:MyPermission1"));
    }

    private static LocalizableString L(string name)
    {
        return LocalizableString.Create<GeoConnectResource>(name);
    }
}
