<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use Prometheus\CollectorRegistry;
use Prometheus\Storage\APCng;

class PrometheusMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $start = microtime(true);

        $response = $next($request);

        $duration = microtime(true) - $start;

        try {
            $registry = new CollectorRegistry(new APCng());

            $counter = $registry->getOrRegisterCounter(
                'laravel',
                'http_requests_total',
                'Total de requests HTTP',
                ['method', 'path', 'status']
            );

            $counter->inc([
                $request->method(),
                $request->path(),
                $response->getStatusCode()
            ]);

            $histogram = $registry->getOrRegisterHistogram(
                'laravel',
                'http_request_duration_seconds',
                'Duración de requests en segundos',
                ['method', 'path'],
                [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
            );

            $histogram->observe($duration, [
                $request->method(),
                $request->path()
            ]);

        } catch (\Exception $e) {
            // No interrumpir el request si Prometheus falla
        }

        return $response;
    }
}
