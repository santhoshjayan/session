using GeoConnect.Localization;
using Volo.Abp.AspNetCore.Mvc;

namespace GeoConnect.Controllers;

/* Inherit your controllers from this class.
 */
public abstract class GeoConnectController : AbpControllerBase
{
    protected GeoConnectController()
    {
        LocalizationResource = typeof(GeoConnectResource);
    }
}
