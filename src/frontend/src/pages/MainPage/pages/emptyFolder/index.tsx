import ForwardedIconComponent from "@/components/genericIconComponent";
import { Button } from "@/components/ui/button";
import { useFolderStore } from "@/stores/foldersStore";

type EmptyFolderProps = {
  setOpenModal: (open: boolean) => void;
};

export const EmptyFolder = ({ setOpenModal }: EmptyFolderProps) => {
  const folders = useFolderStore((state) => state.folders);

  return (
    <div className="m-0 h-full w-full bg-secondary p-0">
      <div className="absolute top-1/2 flex w-full -translate-y-1/2 flex-col items-center justify-center gap-2">
        <h3
          className="font-chivo pt-5 text-2xl font-semibold"
          data-testid="mainpage_title"
        >
          {folders?.length > 1 ? "Empty folder" : "Start building"}
        </h3>
        <p className="pb-5 text-sm text-secondary-foreground">
          Begin with a template, or start from scratch.
        </p>
        <Button
          variant="default"
          onClick={() => setOpenModal(true)}
          id="new-project-btn"
        >
          <ForwardedIconComponent
            name="plus"
            aria-hidden="true"
            className="h-4 w-4"
          />
          <span className="hidden whitespace-nowrap font-semibold md:inline">
            New Flow
          </span>
        </Button>
      </div>
    </div>
  );
};

export default EmptyFolder;
