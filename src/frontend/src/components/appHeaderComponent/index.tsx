import AlertDropdown from "@/alerts/alertDropDown";
import ShadTooltip from "@/components/shadTooltipComponent";
import { CustomOrgSelector } from "@/customization/components/custom-org-selector";
import { CustomProductSelector } from "@/customization/components/custom-product-selector";
import {
  ENABLE_DATASTAX_LANGFLOW,
  ENABLE_NEW_LOGO,
} from "@/customization/feature-flags";
import { useCustomNavigate } from "@/customization/hooks/use-custom-navigate";
import useTheme from "@/customization/hooks/use-custom-theme";
import useAlertStore from "@/stores/alertStore";
import ForwardedIconComponent from "../genericIconComponent";
import { Button } from "../ui/button";
import { Separator } from "../ui/separator";
import ShortDataStaxLogo from "./assets/ShortDataStaxLogo.svg?react";
import ShortLangFlowIcon from "./assets/ShortLangFlowIcon.svg?react";
import { AccountMenu } from "./components/AccountMenu";
import FlowMenu from "./components/FlowMenu";
import GithubStarComponent from "./components/GithubStarButton";

export default function AppHeader(): JSX.Element {
  const notificationCenter = useAlertStore((state) => state.notificationCenter);
  const navigate = useCustomNavigate();
  useTheme();

  return (
    <div className="fixed left-0 top-0 z-[1] flex h-[62px] w-full items-center border-b px-5 py-2.5 dark:bg-black">
      {/* Left Section */}
      <div className="flex w-0 items-center gap-2 lg:w-[20vw] xl:max-w-[325px] 2xl:max-w-[475px]">
        <Button
          unstyled
          onClick={() => navigate("/")}
          className="flex h-8 w-8 items-center"
          data-testid="icon-ChevronLeft"
        >
          {ENABLE_DATASTAX_LANGFLOW ? (
            <ShortDataStaxLogo className="fill-black dark:fill-[white]" />
          ) : ENABLE_NEW_LOGO ? (
            <ShortLangFlowIcon className="h-5 w-5 fill-black dark:fill-[white]" />
          ) : (
            <span className="fill-black text-2xl dark:fill-white">⛓️</span>
          )}
        </Button>
        {ENABLE_DATASTAX_LANGFLOW && (
          <>
            <CustomOrgSelector />
            <CustomProductSelector />
          </>
        )}
      </div>

      {/* Middle Section */}
      <div className="ml-4 mr-auto flex items-center px-5 lg:mx-auto lg:max-lg:w-full">
        <FlowMenu />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-2">
        {!ENABLE_DATASTAX_LANGFLOW && (
          <>
            <Button
              unstyled
              className="flex hidden items-center whitespace-nowrap 2xl:inline"
              onClick={() =>
                window.open("https://github.com/langflow-ai/langflow", "_blank")
              }
            >
              <GithubStarComponent />
            </Button>
          </>
        )}
        <AlertDropdown>
          <ShadTooltip
            content="Notifications and errors"
            side="bottom"
            styleClasses="z-10"
          >
            <Button variant="ghost" className="relative">
              <span
                className={
                  notificationCenter ? `header-notifications-dot` : "hidden"
                }
              />
              <ForwardedIconComponent
                name="bell"
                className="side-bar-button-size h-[18px] w-[18px]"
                aria-hidden="true"
              />
              <span className="hidden whitespace-nowrap lg:inline">
                Notifications
              </span>
            </Button>
          </ShadTooltip>
        </AlertDropdown>
        {!ENABLE_DATASTAX_LANGFLOW && (
          <>
            <ShadTooltip
              content="Go to LangflowStore"
              side="bottom"
              styleClasses="z-10"
            >
              <Button
                variant="ghost"
                className="flex items-center text-sm font-medium"
                onClick={() => navigate("/store")}
                data-testid="button-store"
              >
                <ForwardedIconComponent
                  name="Store"
                  className="side-bar-button-size h-[18px] w-[18px]"
                />
                <span className="hidden whitespace-nowrap lg:inline">
                  Store
                </span>
              </Button>
            </ShadTooltip>
            <Separator
              orientation="vertical"
              className="h-7 dark:border-zinc-700"
            />
          </>
        )}
        {ENABLE_DATASTAX_LANGFLOW && (
          <>
            <ShadTooltip content="Docs" side="bottom" styleClasses="z-10">
              <Button
                variant="ghost"
                className="flex text-sm font-medium"
                onClick={() =>
                  window.open(
                    "https://docs.datastax.com/en/langflow/index.html",
                    "_blank",
                  )
                }
              >
                <ForwardedIconComponent
                  name="book-open-text"
                  className="side-bar-button-size h-[18px] w-[18px]"
                  aria-hidden="true"
                />
                Docs
              </Button>
            </ShadTooltip>
            <ShadTooltip content="Settings" side="bottom" styleClasses="z-10">
              <Button
                data-testid="user-profile-settings"
                variant="ghost"
                className="flex text-sm font-medium"
                onClick={() => navigate("/settings")}
              >
                <ForwardedIconComponent
                  name="Settings"
                  className="side-bar-button-size h-[18px] w-[18px]"
                />
                Settings
              </Button>
            </ShadTooltip>
            <Separator
              orientation="vertical"
              className="h-7 dark:border-zinc-700"
            />
          </>
        )}
        <div className="ml-5 flex">
          <AccountMenu />
        </div>
      </div>
    </div>
  );
}
