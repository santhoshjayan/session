using System;
using System.Collections.Generic;
using System.Text;
using GeoConnect.Localization;
using Volo.Abp.Application.Services;

namespace GeoConnect;

/* Inherit your application services from this class.
 */
public abstract class GeoConnectAppService : ApplicationService
{
    protected GeoConnectAppService()
    {
        LocalizationResource = typeof(GeoConnectResource);
    }
}
