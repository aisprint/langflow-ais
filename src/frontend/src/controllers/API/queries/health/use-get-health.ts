import {
  REFETCH_SERVER_HEALTH_INTERVAL,
  SERVER_HEALTH_INTERVAL,
} from "@/constants/constants";
import { useUtilityStore } from "@/stores/utilityStore";
import { keepPreviousData } from "@tanstack/react-query";
import { useQueryFunctionType } from "../../../../types/api";
import { api } from "../../api";
import { UseRequestProcessor } from "../../services/request-processor";

interface getHealthResponse {
  status: string;
  chat: string;
  db: string;
  folder: string;
  variables: string;
}

export const useGetHealthQuery: useQueryFunctionType<
  undefined,
  getHealthResponse
> = (_, options) => {
  const { query } = UseRequestProcessor();
  const setHealthCheckTimeout = useUtilityStore(
    (state) => state.setHealthCheckTimeout,
  );
  const healthCheckTimeout = useUtilityStore(
    (state) => state.healthCheckTimeout,
  );
  /**
   * Fetches the health status of the API.
   *
   * @returns {Promise<AxiosResponse<TransactionsResponse>>} A promise that resolves to an AxiosResponse containing the health status.
   */
  async function getHealthFn() {
    try {
      const timeoutPromise = new Promise<never>((_, reject) =>
        setTimeout(
          () => reject(new Error("Request timed out")),
          SERVER_HEALTH_INTERVAL,
        ),
      );
      const apiPromise = api.get<{ data: getHealthResponse }>("/health");
      const response = await Promise.race([apiPromise, timeoutPromise]);
      setHealthCheckTimeout(null);
      return response.data;
    } catch (error) {
      const isUnhealthy =
        error &&
        typeof error === "object" &&
        "response" in error &&
        healthCheckTimeout === null;

      if (isUnhealthy) {
        setHealthCheckTimeout("unhealthy");
      } else if (healthCheckTimeout === null) {
        setHealthCheckTimeout("timeout");
      }
      throw error;
    }
  }

  const queryResult = query(["useGetHealthQuery"], getHealthFn, {
    placeholderData: keepPreviousData,
    refetchInterval: REFETCH_SERVER_HEALTH_INTERVAL,
    retry: false,
    ...options,
  });

  return queryResult;
};
