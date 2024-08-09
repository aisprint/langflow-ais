import { usePatchUpdateFlow } from "@/controllers/API/queries/flows/use-patch-update-flow";
import useAlertStore from "@/stores/alertStore";
import useFlowsManagerStore from "@/stores/flowsManagerStore";
import useFlowStore from "@/stores/flowStore";
import { FlowType } from "@/types/flow";

const useSaveFlow = () => {
  const flows = useFlowsManagerStore((state) => state.flows);
  const setFlows = useFlowsManagerStore((state) => state.setFlows);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const reactFlowInstance = useFlowStore((state) => state.reactFlowInstance);
  const nodes = useFlowStore((state) => state.nodes);
  const edges = useFlowStore((state) => state.edges);
  const setSaveLoading = useFlowsManagerStore((state) => state.setSaveLoading);
  const setCurrentFlow = useFlowStore((state) => state.setCurrentFlow);

  const currentFlow = useFlowStore((state) => state.currentFlow);
  const flowData = currentFlow?.data;

  const { mutate } = usePatchUpdateFlow();

  const saveFlow = async (flow?: FlowType): Promise<void> => {
    setSaveLoading(true);
    return new Promise<void>((resolve, reject) => {
      if (currentFlow) {
        flow = flow || {
          ...currentFlow,
          data: {
            ...flowData,
            nodes,
            edges,
            viewport: reactFlowInstance?.getViewport() ?? {
              zoom: 1,
              x: 0,
              y: 0,
            },
          },
        };
      }
      if (flow && flow.data) {
        const { id, name, data, description, folder_id, endpoint_name } = flow;
        mutate(
          { id, name, data, description, folder_id, endpoint_name },
          {
            onSuccess: (updatedFlow) => {
              setSaveLoading(false);
              if (updatedFlow !== null) {
                // updates flow in state
                setFlows(
                  flows.map((flow) => {
                    if (flow.id === updatedFlow.id) {
                      return updatedFlow;
                    }
                    return flow;
                  }),
                );
                setCurrentFlow(updatedFlow);
                resolve();
              }
            },
            onError: (e) => {
              setErrorData({
                title: "Failed to save flow",
                list: [e.message],
              });
              setSaveLoading(false);
              reject(e);
            },
          },
        );
      } else {
        reject(new Error("Flow not found"));
      }
    });
  };

  return saveFlow;
};

export default useSaveFlow;
